# this file scrapes the entire Mark Manson archive
# and adds these properties to the links –
# featured-image:  wp-post-image img
# title: sailthru.title
# description: article-card__standfirst
# tags: article-card__topic
# publication date: sailthru.date

import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp

archive_links = []
def pull_archive():
    root_link = "https://markmanson.net"
    count = 0
    headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
            'From': 'buzo@buzo.xyz'
        }
    r = requests.get(root_link + "/archive", headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    links = soup.find_all('td')

    for c in links:
        x = c.find_all('a')
        if x!= []:
            new_values = {'language': 'EN', 'site': 'Mark Manson', 
                        'tags': 'Life Advice, Philosophy', 'description': '',
                        'image': 'https://markmanson.net/wp-content/uploads/2016/05/audio-album-cover-2.png'}
            if 'video' in str(x[0]) or 'Subscribers Only' in str(x[0]):
                continue
            new_values['title'] = x[0].find('span').contents[0]
            new_values['url'] = root_link + x[0]['href']
            count += 1
            new_values['serial'] = str(count)
            archive_links.append(new_values)
    return len(archive_links)

pull_archive()
import json
with open('markmanson.json', 'w+') as f:
    json.dump(archive_links, f)