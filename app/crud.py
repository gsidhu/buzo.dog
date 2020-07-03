
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

### CREATE DATABASE
def create():
    try:
        counter = list(mycol.find().sort("_id",-1))[0]['_id']
    except:
        counter = 0

    links = []
    
    # # stray sites
    # links.append({"Random": sources.sites})

    # # regular scraps - pinboard
    # links.append({"Pinboard": scrape.pinboard_load()})

    # # subreddits
    # temp = []
    # for i in sources.subreddits:
    #     temp.extend(scrape.reddit_subreddit_url_extracter(i))
    # links.append({"Reddit Subs": temp})
    
    # reddit threads
    temp = []
    for i in sources.reddit_threads:
        temp.extend(scrape.reddit_url_extracter(i))
    links.append({"Reddit threads": temp})

    ## dd is the dict inside links
    for dd in links:
        key = list(dd.keys())[0]
        print(key)
        for l in dd[key]:
            counter += 1

            ## get metadata
            metadata = curate.curate(l)
            if metadata == 'remove':
                continue
            collection = {
                        "_id":counter,
                        'link': l,
                        'source': key,
                        'likes': 0,
                        'dislikes': 0
                        }
            collection = {**collection, **metadata}
            mycol.insert_one(collection)

            if counter % 50 == 0:
                print(counter, " links added.")

### READ DATABASE
def read(count=1, **kwargs):
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

if __name__ == '__main__':
    ############################
    # Command line utility
    ############################
    parser = argparse.ArgumentParser(
        description="Creates, reads, updates and deletes the mongodatabase.")

    # Call the create function
    parser.add_argument("-c", "--create", help="load the DB with latest links",
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
