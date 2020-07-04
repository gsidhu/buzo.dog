# this file scrapes the entire Aeon.co archive of essays
# and adds these properties to the links –
# featured-image: <figure style url bg image>
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
    root_link = "https://aeon.co"
    count = 0
    for d in range(1,54):
        l = root_link + "/essays/popular?page=" + str(d)
        print('Looking at page ', str(d), '...', sep='')
        print('URL:', l)
        r = requests.get(l)
        soup = BeautifulSoup(r.content, 'html.parser')

        inner_count = 0
        for link in soup.find_all('div', class_="gutter--inner"):
            new_values = {'language': 'EN', 'site': 'Aeon'}
            new_values['title'] = link.find_all('a')[0].contents[0]

            fig_tag = soup.find_all('figure', class_="responsive-image")[inner_count]['style']
            new_values['image'] = fig_tag[(fig_tag.find('url')+5):-2]
            
            new_values['description'] = link.find_all('h2')[0].contents[0].strip()
            
            new_values['tags'] = link.find_all('span', class_='article-card__topic')[0].contents[0]

            new_values['url'] = root_link + link.find_all('a')[0]['href']
            
            inner_count += 1
            count += 1
            new_values['serial'] = str(count)
            archive_links.append(new_values)
    return len(archive_links)
pull_archive()

import json
with open('aeon_dump.json', 'w+') as f:
    json.dump(archive_links, f)