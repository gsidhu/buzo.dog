
import pymongo
myclient = pymongo.MongoClient('127.0.0.1', 27017)
mydb = myclient['buzodog']
mycol = mydb['core']

import argparse
import logging as log

import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp 

try:
    from . import sources
    from . import scrape
    from . import curate
except:
    import sources
    import scrape
    import curate

# dumps = ['./scrapers/xkcd_dump.json', './scrapers/aeon_dump.json', 
#         './scrapers/bp_dump.json', './scrapers/bp_dump1.json', 
#         './scrapers/margins_dump.json', './scrapers/links_on_margins_dump.json',
#         './scrapers/threewordphrase_dump.json', './scrapers/stratechery_dump.json', './scrapers/markmanson_dump.json']

dumps = ['./scrapers/fsblog_culture_dump.json',
'./scrapers/fsblog_decision-making_dump.json',
'./scrapers/fsblog_mental-models_dump.json',
'./scrapers/fsblog_science_dump.json',
'./scrapers/fsblog_thinking_dump.json',
'./scrapers/fsblog_uncategorized_dump.json',
'./scrapers/fsblog_writing_dump.json']

### Create a backup
def backup():
    mycol = mydb['core']

    # create backup
    mycol.aggregate([
        {"$match": {}}, 
        {"$out": "backup"},
    ])

### Restore backup
def restore():
    mycol = mydb['backup']

    # create backup
    mycol.aggregate([
        {"$match": {}}, 
        {"$out": "core"},
    ])

### CREATE DATABASE
def create():
    try:
        counter = list(mycol.find().sort("_id",-1))[0]['_id']
    except:
        counter = 0

    import ast
    for filename in dumps:
        with open(filename) as f:
            text = f.read()
            links = ast.literal_eval(text)
        
        print(filename)
        ## dd is the dict inside links
        for dd in links:
            counter += 1

            ## get metadata
            # metadata = curate.curate(l)
            # if metadata == 'remove':
            #     continue

            collection = {
                        "_id":counter,
                        'link': dd['url'],
                        'source': dd['site'],
                        'language': dd['language'],
                        'tags': dd['tags'],
                        'description': dd['description'],
                        'image': dd['image'],
                        'title': dd['title'],
                        'likes': 0,
                        'dislikes': 0
                        }
            mycol.insert_one(collection)

            if counter % 50 == 0:
                print(counter, " links added.")

### READ DATABASE
def read(count=1, give_sources=0, **kwargs):
    args = []
    for i in kwargs.keys():
        args.append({i: kwargs[i]})
    
    if len(args) > 0:
        pipeline = [
                {"$match": {"$and": args}},
                {"$sample": {"size": count}}
            ]
    else:
        pipeline = [ 
                {"$sample": {"size": count}}
            ]

    result = list(mycol.aggregate(pipeline))

    return result

### UPDATE DATABASE

if __name__ == '__main__':
    ############################
    # Command line utility
    ############################
    parser = argparse.ArgumentParser(
        description="Creates, reads, updates and deletes the mongodatabase.")

    # Call the create function
    parser.add_argument("-c", "--create", help="load the DB with latest links",
                        action="store_true")

    # Call the create function
    parser.add_argument("-b", "--backup", help="backup the DB",
                        action="store_true")

    # Call the create function
    parser.add_argument("-r", "--restore", help="restore the backup",
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

    if args.create:
        create()
    if args.backup:
        backup()
    if args.restore:
        restore()
