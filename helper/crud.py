import pymongo
import urllib.parse

import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp 

# Log into DB 
username = urllib.parse.quote_plus('') # defined in env
password = urllib.parse.quote_plus('') # defined in env
myclient = pymongo.MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password), 27017)
mydb = myclient['buzodog']
mycol = mydb['cache']

# 