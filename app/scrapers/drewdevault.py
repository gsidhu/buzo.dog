# this file scrapes the entire Drew Devault Blog archive
# and adds these properties to the links –
# featured-image:  wp-post-image img
# title: sailthru.title
# description: article-card__standfirst
# tags: article-card__topic
# publication date: sailthru.date

import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp

# import metadata_parser

archive_links = []
def pull_archive():
    root_link = "https://drewdevault.com/"
    count = 0
    r = requests.get(root_link)
    soup = BeautifulSoup(r.content, 'html.parser')
    links = soup.find_all('div', class_="article")

    for c in links:
        new_values = {'language': 'EN', 'site': 'Drew Devault\'s Blog', 
                    'tags': 'Tech, Internet, Opinion', 'description': '',
                    'image': 'https://drewdevault.com/avatar-148.jpg'}

        new_values['title'] = c.find_all('a')[0].contents[0]
        new_values['url'] = c.find_all('a')[0]['href']
        count += 1
        new_values['serial'] = str(count)
        archive_links.append(new_values)
    return len(archive_links)
pull_archive()
import json
with open('drewdevault_dump.json', 'w+') as f:
    json.dump(archive_links, f)