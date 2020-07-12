# this file scrapes the entire The Word Phrase archive
# and adds these properties to the links –
# featured-image:  wp-post-image img
# title: sailthru.title
# description: article-card__standfirst
# tags: article-card__topic
# publication date: sailthru.date

import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp

import metadata_parser

archive_links = []
def pull_archive():
    root_link = "http://threewordphrase.com/"
    count = 0
    r = requests.get(root_link + "archive.htm")
    soup = BeautifulSoup(r.content, 'html.parser')
    links = soup.find_all('span', class_="links")

    for c in links[0].find_all('a'):
        new_values = {'language': 'EN', 'site': 'Three Word Phrase', 
                    'tags': 'Comic', 'description': '',
                    'image': 'http://threewordphrase.com/header.gif'}

        new_values['title'] = c.contents[0]
        new_values['url'] = root_link + c['href']
        count += 1
        new_values['serial'] = str(count)
        archive_links.append(new_values)
    return len(archive_links)
pull_archive()
import json
with open('threewordphrase_dump.json', 'w+') as f:
    json.dump(archive_links, f)