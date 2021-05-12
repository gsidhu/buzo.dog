import pymongo
import urllib.parse
username = urllib.parse.quote_plus('thatgurjot') # defined in env
password = urllib.parse.quote_plus('fz*NJPrbkypUMU@*@FanqRe65T2') # defined in env
myclient = pymongo.MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password), 27017)
# myclient = pymongo. MongoClient('mongodb://127.0.0.1', 27017)
mydb = myclient['buzodog']

import argparse
import logging as log

import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp 

try:
    import cache
    import helper
except:
    from . import cache
    from . import helper

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
    mycol = mydb['cache']
    try:
        counter = list(mycol.find({}, {"link": 1}).limit(1).sort([('$natural', -1 )]))[0]['_id']
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

### FETCH LINK DETAILS
def fetch(url):
    mycol = mydb['cache']
    # check if url already exists
    # TODO: replace this with an actual fuzzy search function because links can have trailing slashes and such
    pipeline = [{"$match": {"link": url}}]
    struct = list(mycol.aggregate(pipeline))
    if len(struct) == 0:
        struct = cache.cache_art(url)
    else:
        struct = struct[0]
        struct['exists'] = True
    # add description if missing
    if struct['description'] == '':
        struct['description'] = struct['text'][:350]
    return struct
    

### ADD TO DATABASE
def add(collection):
    from datetime import datetime
    from hashids import Hashids
    hashids = Hashids(min_length=12, salt='thatbuzo')

    mycol = mydb['cache']
    try:
        counter = list(mycol.find({}, {"link": 1}).limit(1).sort([('$natural', -1 )]))[0]['_id']
        counter = int(hashids.decode(counter)[0])
    except:
        counter = 0

    counter += 1
    collection['date_added'] = datetime.today().strftime('%Y-%m-%d')
    collection['_id'] = hashids.encode(counter)
    collection['likes'] = 0

    mycol.insert_one(collection)
    return collection['_id']

### READ DATABASE
def read(count=1, give_sources=0, **kwargs):
    mycol = mydb['cache']
    args = []
    for i in kwargs.keys():
        args.append({i: kwargs[i]})

    if 'source' in kwargs.keys() and kwargs['source'] == 'Recent':
        result = list(mycol.find({}).limit(count).sort([('$natural', -1 )]))
    else:
        if 'source' in kwargs.keys() and kwargs['source'] == 'Favourite':
            args[0]['likes'] = 1
            del args[0]['source']

        if 'db' in kwargs.keys():
            mycol = mydb[kwargs['db']]

        if 'id' in kwargs.keys():
            pipeline = [{"$match": {"_id": kwargs['id']}}]
        elif 'link' in kwargs.keys():
            pipeline = [{"$match": {"link": kwargs['link']}}]
        else:
            if len(args) > 0:
                pipeline = [
                        {"$match": {"$and": args}},
                        {"$sample": {"size": count}}
                    ]
            else:
                pipeline = [ {"$sample": {"size": count}} ]
        result = list(mycol.aggregate(pipeline))

    return result

### UPDATE DATABASE
def update(collection):
    mycol = mydb['cache']

    myquery = { "_id": collection["_id"] }

    newvalues = { "$set": { 
        "title": collection['title'],
        'source': collection['source'],
        'description': collection['description'],
        'tags': collection['tags'],
        'language': collection['language'],
        'author': collection['author']
        } }
    try:
        mycol.update_one(myquery, newvalues)
        return True
    except:
        return False

# DELETE ITEM
def delete(iD):
    mycol = mydb['cache']

    myquery = { "_id": iD }
    try:
        mycol.delete_one(myquery)
        return True
    except:
        return False

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
