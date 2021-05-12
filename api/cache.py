# This script reads a link, pulls its article text and other metadata
# and then saves it in the 'cached' collection in the dB
# It has the following wrapper functions –
# 1. Do it for all links in the 'core' collection 
# 2. Do it for a single link 
# 3. Store the cached article in the dB

import pymongo
myclient = pymongo.MongoClient('127.0.0.1', 27017)
mydb = myclient['buzodog']
mycol = mydb['cached']

import argparse
import logging as log

from hashids import Hashids
hashids = Hashids(min_length=12, salt='thatbuzo')

import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp 

try:
    from . import helper
except:
    import helper

### Create a backup
def backup():
    mycol = mydb['cache']

    # create backup
    mycol.aggregate([
        {"$match": {}}, 
        {"$out": "backup_cache"},
    ])

### Restore backup
def restore():
    mycol = mydb['backup_cache']

    # create backup
    mycol.aggregate([
        {"$match": {}}, 
        {"$out": "cache"},
    ])

def cache_art(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
        'From': 'buzo@buzo.dog'
    }

    from newspaper import Config
    from newspaper import Article

    config = Config()
    config.browser_user_agent = headers['User-Agent']
    article = Article(url, keep_article_html=True, config=config)
    article.download()
    
    article.parse()
    struct = {
        'html': article.article_html,
        'link': url,
        'author': article.authors,
        'pubdate': article.publish_date,
        'text': article.text,
        'title': article.title,
        'image': article.top_image,
        'description': article.meta_description
    }
    
    return struct

### CREATE DATABASE
def create_cache():
    try:
        # fetch the last document's id
        counter = list(mycol.find({}, {"link": 1}).limit(1).sort([('$natural', -1 )]))[0]['_id']
        counter = int(hashids.decode(counter)[0])
    except:
        # if empty collection then start afresh
        counter = 0
    
    print('Starting at %s' % str(counter))

    import ast
    for filename in dumps:
        with open(filename) as f:
            text = f.read()
            links = ast.literal_eval(text)
        
        print(filename)
        ## dd is the dict inside links
        for dd in links:
            counter += 1
            try:
                struct = cache_art(dd['url'])
            except Exception as e:
                print(repr(e))
                print("failed to cache url: %s" % dd['url'])
                continue
            collection = {
                        "_id": hashids.encode(counter),
                        'link': dd['url'],
                        'source': dd['site'],
                        'language': dd['language'],
                        'tags': dd['tags'],
                        'description': dd['description'],
                        'logo': dd['image'],
                        'title': dd['title'],
                        'likes': 0,
                        'dislikes': 0,
                        'html': struct['html'],
                        'rawhtml': struct['rawhtml'],
                        'author': struct['author'],
                        'pubdate': struct['pubdate'],
                        'text': struct['text'],
                        'image': struct['image'],
                        'buzotext': struct['buzotext']
                        }
            # set first paragraph of text as description
            if collection['description'] == '':
                try:
                    collection['description'] = collection['buzotext'].splitlines()[0]
                    if collection['description'].lower() == collection['title'].lower():
                        collection['description'] = collection['buzotext'].splitlines()[1]
                except:
                    pass

            if collection['author'] == []:
                try:
                    collection['author'] = dd['author']
                except:
                    collection['author'] = dd['site']
            
            mycol.insert_one(collection)
            print("%s cached" % dd['url'])
            if counter % 50 == 0:
                print("%s links cached" % counter)
        print("Total %s links cached" % len(links))

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
        description="Creates, reads, updates and deletes the cached article database.")

    # Call the create function
    parser.add_argument("-c", "--create", help="store the cached article",
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
        create_cache()
    if args.backup:
        backup()
    if args.restore:
        restore()
