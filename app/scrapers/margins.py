# this file scrapes the entire Margins archive
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
    count = 0
    with open('/Users/thatgurjot/Git Repos/buzo.xyz/app/scrapers/margins.html', 'r+') as f:
        r = f.read()
    soup = BeautifulSoup(r, 'html.parser')
    links1 = soup.find_all('a', class_="post-preview-title")
    links2 = soup.find_all('a', class_="post-preview-description")
    links3 = soup.find_all('div', class_="post-preview-image")

    for c in range(len(links1)):
        if c%2 == 0:
            continue
        new_values = {'language': 'EN', 'site': 'Margins', 
                    'tags': 'Opinion'}
        z = links1[c]
        new_values['title'] = z.contents[0]
        new_values['url'] = z['href']

        z = links2[c]
        new_values['description'] = z.contents[0]

        try:
            z = links3[c]
            new_values['image'] = z['style'][23:-3]
        except:
            new_values['image'] = 'https://cdn.substack.com/image/fetch/w_96,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F6fc17be7-df3b-43ce-b8c2-4388c0a27d1f_250x250.png'

        count += 1
        new_values['serial'] = str(count)
        archive_links.append(new_values)
    return len(archive_links)
pull_archive()

import json
with open('margins_dump.json', 'w+') as f:
    json.dump(archive_links, f)