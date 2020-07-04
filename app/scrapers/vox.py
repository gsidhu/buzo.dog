# this file scrapes the entire Vox.com archive of articles
# and adds these properties to the links –
# featured-image: sailthru.image.full
# title: sailthru.title
# description: sailthru.description
# tags: sailthru.tags
# publication date: sailthru.date

import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp

import metadata_parser

archive_links = []

def pull_archive():
    new_values = {
        'title': '',
        'image': '',
        'description': '',
        'keywords': '',
        'tags': '',
        'url': '',
        'language': 'EN',
        'site': 'Vox',
        'serial': 0
    }
    
    root_link = "https://www.vox.com/archives/"
    year = [i for i in range(2014, 2015)]
    month = [i for i in range(1, 13)]
    for y in year:
        for m in month:
            for d in range(1,32):
                print("Now running:", m, ",", y, ": Page", d)
                l = root_link + str(y) + "/" + str(m) + "/" + str(d)
                try:
                    r = requests.get(l)
                    soup = BeautifulSoup(r.content, 'html.parser')

                    for link in soup.find_all('h2', class_="c-entry-box--compact__title"):
                        archive_links.append(link.find_all('a', href=True)[0]['href'])
                except:
                    pass
    
    return len(archive_links)

    # print("Fetching metadata from site...")
    # try:
    #     page = metadata_parser.MetadataParser(url=link, search_head_only=True)
    #     metas = list(page.metadata['meta'].keys())
    #     for i in metas:
    #         for k in list(new_values.keys()):
    #             if k in i and new_values[k] == '':
    #                 new_values[k] = page.metadata['meta'][i]
    # except:
    #     # in case the link returns a 400-404 error
    #     pass

    # return links

with open('vox1.csv', 'w+') as f:
    for i in archive_links:
        l = i + ',\n'
        f.write(l)
import json 