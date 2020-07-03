import argparse
import logging as log

import requests
from bs4 import BeautifulSoup
import metadata_parser
from pprint import pprint as pp 

# bing search
bing_access_key = '7b91e82ce3dd42739def457cba384114'
key2 = '3ecd93fc26244578a1c9b80fa581fbe8'
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
headers = {"Ocp-Apim-Subscription-Key": bing_access_key}

def removeDuplicates():
    import pymongo 
    myclient = pymongo.MongoClient('127.0.0.1', 27017)
    mydb = myclient['buzodog']
    mycol = mydb['core']

    # create backup
    mycol.aggregate([
        {"$match": {}}, 
        {"$out": "backup"},
    ])

    # remove duplicates based on links
    mycol.aggregate([ 
        { "$sort": { "_id": 1 } }, 
        { "$group": { 
            "_id": "$link", 
            "doc": { "$first": "$$ROOT" } 
        }}, 
        { "$replaceRoot": { "newRoot": "$doc" } },
        { "$out": "core" }
    ])

    # renumber the ids
    count = 0
    for x in mycol.find().sort("_id",1):
        count += 1
        myquery = { "_id": x['_id'] }
        new_values = { "$set": {"id": count} }
        x = mycol.update_one(myquery, new_values)
    
    print(count, " documents renumbered.")

def removeTrash():
    import pymongo 
    myclient = pymongo.MongoClient('127.0.0.1', 27017)
    mydb = myclient['buzodog']
    mycol = mydb['core']

    trash = [1, 79, 88, 89, 100, 111, 128, 150, 147, 159, 175, 200, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 585, 586, 589, 590, 591, 640, 644, 649, 659, 661, 662, 663, 719, 746, 759, 760, 761, 763, 764, 779, 785, 789, 793, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892]
    
    # remove trash links based on id
    for i in trash:
        myquery = { "id": i }
        mycol.delete_one(myquery) 

    # renumber the ids
    count = 0
    for x in mycol.find().sort("_id",1):
        count += 1
        myquery = { "_id": x['_id'] }
        new_values = { "$set": {"id": count} }
        x = mycol.update_one(myquery, new_values)
    
    print(count, " documents renumbered.")

def curate(link, scratch=1):
    if scratch:
        new_values = {
            'title': '',
            'image': '',
            'description': '',
            'keywords': '',
            'tags': '',
            'safe': True,
            'language': ''
        }
    else:
        new_values = scratch

    ## Fetch metadata from site
    # eg. i = og:title, k = title
    # then new_values['title'] = valueOf('og:title')
    print("Fetching metadata from site...")
    try:
        page = metadata_parser.MetadataParser(url=link, search_head_only=True)
        metas = list(page.metadata['meta'].keys())
        for i in metas:
            for k in list(new_values.keys()):
                if k in i and new_values[k] == '':
                    new_values[k] = page.metadata['meta'][i]
    except:
        # in case the link returns a 400-404 error
        pass

    ## Fetch image by parsing site source code
    ## if image not available from metadata
    ## if this fails set buzo image as default
    if new_values['image'] == '' or new_values['image'] == None:
        print("Fetching display image from site...")
        try:
            r = requests.get(link)
        except:
            return 'remove'
        soup = BeautifulSoup(r.content, 'html.parser')
        try:
            new_values['image'] = soup.find_all('img')[0].get('src')
        except:
            new_values['image'] = 'https://buzo.dog/img/buzo.976a216d.png'

    ## Fetch metadata from Bing
    ## if title or description is missing
    if new_values['title'] == '' or new_values['description'] == '':
        print("Trying to fetch metadata from Bing...")
        search_term = link
        params = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()

        for result in search_results['webPages']['value']:
            if result['url'] == link:
                new_values['title'] = result['name']
                new_values['description'] = result['snippet']
                new_values['nsfw'] = result['isFamilyFriendly']
                new_values['language'] = result['language']

    return new_values

def clean():
    import pymongo 
    myclient = pymongo.MongoClient('127.0.0.1', 27017)
    mydb = myclient['buzodog']
    mycol = mydb['core']

    for x in mycol.find():
        if 'title' not in x.keys() or x['title'] == '' or x['description'] == '':
            print("Updating missing fields...")
            new_values = curate(x['link'])
            if new_values == 'remove':
                print("Removing unwanted links...")
                myquery = { "_id": x['_id'] }
                mycol.delete_one(myquery)
                continue
            if new_values['title'] != '':
                myquery = { "_id": x['_id'] }
                new_values = { "$set": new_values }
                x = mycol.update_one(myquery, new_values)
                continue

        if 'title' in x.keys() and 'description' in x.keys():
            if 'rafael' in x['title'].lower() or 'rafael' in x['description'].lower() or 'askreddit' in x['link'].lower():
                print("Removing unwanted links...")
                myquery = { "_id": x['_id'] }
                mycol.delete_one(myquery) 
                continue
        try:
            x['description'] = x['description'].strip()
        except:
            print("Removing unwanted links...")
            myquery = { "_id": x['_id'] }
            mycol.delete_one(myquery)
            continue

if __name__ == '__main__':
    ############################
    # Command line utility
    ############################
    parser = argparse.ArgumentParser(
        description="Creates, reads, updates and deletes the mongodatabase.")

    # Call the removeDuplicates function
    parser.add_argument("-rd", "--removedupes", help="remove duplicate documents from the DB", action="store_true")

    # Call the removeDuplicates function
    parser.add_argument("-rt", "--removetrash", help="remove trash links from the DB", action="store_true")

    # Call the curate function
    # parser.add_argument("-c", "--curate", help="add site metadata to documents", action="store_true")

    # Call the clean function
    parser.add_argument("-cl", "--clean", help="clean up documents", action="store_true")

    # Verbosity and Debugging
    parser.add_argument(
        '-d', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=log.DEBUG,
        default=log.WARNING,
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Be verbose",
        action="store_const", dest="loglevel", const=log.INFO,
    )

    args = parser.parse_args()
    log.basicConfig(level=args.loglevel)

    if args.removedupes:
        removeDuplicates()
    if args.removetrash:
        removeTrash()
    if args.clean:
        clean()
