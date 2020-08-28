# this file scrapes the entire xkcd archive
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
    root_link = "https://xkcd.com"
    count = 0
    r = requests.get(root_link + "/archive/")
    soup = BeautifulSoup(r.content, 'html.parser')
    links = soup.find_all('div', id="middleContainer")

    for c in links[0].find_all('a'):
        new_values = {'language': 'EN', 'site': 'xkcd', 
                    'tags': 'Comic', 'description': '',
                    'image': 'https://xkcd.com/s/0b7742.png'}

        new_values['title'] = c.get_text()
        # if len(c.contents) > 1:
        #     new_values['title'] = ''
        #     for j in c.contents:
        #         try:
        #             new_values['title'] += j
        #         except:
        #             new_values['title'] += j.contents[0]
        new_values['url'] = root_link + c['href']
        count += 1
        new_values['serial'] = str(count)
        archive_links.append(new_values)
    return len(archive_links)
pull_archive()
import json
with open('xkcd.json', 'w+') as f:
    json.dump(archive_links, f)