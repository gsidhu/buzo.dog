## Seminar
## read the rawhtml and extract the article
## and turn it into a md file on disk

import pymongo
myclient = pymongo.MongoClient('127.0.0.1', 27017)
mydb = myclient['buzodog']
mycol = mydb['seminar']

# import requests

import argparse
import logging as log

try:
    from . import helper 
except:
    import helper 

def get_article():
    count = 0
    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0", 'From': 'buzo@buzo.dog'}
    skip = [91, 1185, 1187, 1189, 2627, 2706, 2761, 2917]
    for article in mycol.find():
        count += 1
        if count in skip or count < 0:
            continue
        url = article['link']
        # r = requests.get(url, headers=headers)
        # raw = r.content
        raw = article['rawhtml']
        title = article['title']
        try:
            text = helper.scrape(raw, 'html5lib', url, title)
            text = text.replace('\\r\\n', '')
            text = text.replace('\\x91', "'")
            text = text.replace('\\x92', "'")
            text = text.replace('\\x85', '...')
            text = text.replace('\\x96', "-")
        except:
            # print(count)
            # print(url)
            # print("\n\n****\n\n")
            # error 
            skip.append(count)
            continue

        myquery = { "link": url }
        # update text 
        newvalues = { "$set": { "buzotext": text } }
        mycol.update_one(myquery, newvalues)

        # update rawhtml
        # newvalues = { "$set": { "rawhtml": raw } }
        # mycol.update_one(myquery, newvalues)

        metadata = {'title': str('"' + article['title'].replace('"', "'") + '"'),
        'date': '2000-01-01T00:00:00+05:30',
        'draft': 'false',
        'tags': str('["' + article['issue_num'] + '"]'),
        'categories': str('["' + article['year'] + '"]'),
        'issue_name': str('"' + article['issue_title'] + '"'),
        'issue_focus': str('"' + article['description'] + '"'),
        'issue_cover': str('"' + article['image'] + '"'),
        'issue_cover_credits': str('"' + article['image_credits'] + '"')}

        filename = article['title'].translate(str.maketrans({' ': '_', ':': '_', '/': '_', '\\': '_', ',': '', '"': '', "'": ''}))
        filename = filename.replace("__", '_')
        filename = str(count) + "_" + article['issue_num'] + '_' + filename + '.md'
        
        ## title replace 
        fm_title = article['title'].replace('"', "'").lower()
        temp = text[:200].lower()

        if fm_title in temp:
            findex = temp.find(fm_title)
            text = text[:findex] + text[findex+len(fm_title):]

        create_md(metadata, text, filename)

        if count % 10 == 0:
            print("%s articles scraped" % count)
    
    with open('./skip.txt', 'w+') as f:
        f.write(str(skip))

    return True

def create_md(metadata, text, filename):
    content = '---\n'
    for key in metadata.keys():
        content += key + ": " + metadata[key] + "\n"
    content += '---\n'
    content += text

    with open(str('./articles/' + filename), 'w+') as f:
        f.write(content)
    
if __name__ == '__main__':
    ############################
    # Command line utility
    ############################
    parser = argparse.ArgumentParser(
        description="Creates, reads, updates and deletes the cached article database.")

    # Call the create function
    parser.add_argument("-g", "--get", help="store the cached article",
                        action="store_true")

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

    if args.get:
        get_article()
