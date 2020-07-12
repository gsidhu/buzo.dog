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

archive_links = []
def pull_archive():
    root_link = "https://stratechery.com/category/articles/page/"
    count = 0
    for d in range(1,42):
        l = root_link + str(d) + "/"
        print('Looking at page ', str(d), '...', sep='')
        print('URL:', l)
        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
            'From': 'buzo@buzo.dog'
        }
        r = requests.get(l, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        inner_count = 0
        for link in soup.find_all('h1', class_="entry-title"):
            new_values = {'language': 'EN', 'site': 'Statechery', 'image': 'https://stratechery.com/wp-content/themes/stratechery-theme/images/mobile-logo-600-82.png',
            'tags': 'Tech, Business'}
            new_values['title'] = str(link.find('a').contents[0])
            new_values['url'] = str(link.find('a')['href'])

            des_tag = soup.find_all('div', class_="entry-content")
            
            new_values['description'] = str(des_tag[inner_count].find('p').contents[0])

            inner_count += 1
            count += 1
            new_values['serial'] = str(count)
            archive_links.append(new_values)
    return len(archive_links)
pull_archive()

import json
with open('stratechery_dump.json', 'w+') as f:
    json.dump(archive_links, f)