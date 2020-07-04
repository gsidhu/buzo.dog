# this file scrapes the entire Brain Pickings 'culture' archive
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
    root_link = "https://www.brainpickings.org/tag/culture/page/"
    count = 0
    for d in range(293,724):
        l = root_link + str(d) + "/"
        print('Looking at page ', str(d), '...', sep='')
        print('URL:', l)
        r = requests.get(l)
        soup = BeautifulSoup(r.content, 'html.parser')
        left_side = soup.find_all('div', class_="recent_archives_left")[0]
        right_side = soup.find_all('div', class_="recent_archives_right")[0]
        for i in range(len(left_side.find_all('a', class_="yellow"))):
            new_values = {'language': 'EN', 'site': 'Brain Pickings', 'tags': 'Culture'}
            new_values['title'] = left_side.find_all('a', class_="yellow")[i].contents[0]
            if len(left_side.find_all('a', class_="yellow")[i].contents) > 1:
                new_values['title'] = ''
                for j in left_side.find_all('a', class_="yellow")[i].contents:
                    try:
                        new_values['title'] += j
                    except:
                        new_values['title'] += j.contents[0]
            try:
                new_values['image'] = left_side.find_all('img', class_="wp-post-image")[1]['src']
            except:
                new_values['image'] = left_side.find_all('img')[1]['src']
            try:
                new_values['description'] = left_side.find_all('h2')[1].contents[0]
            except:
                new_values['description'] = ''
            new_values['url'] = left_side.find_all('a', class_="yellow")[i]['href']
            count += 1
            new_values['serial'] = str(count)
            archive_links.append(new_values)
        for i in range(len(right_side.find_all('a', class_="yellow"))):
            new_values = {'language': 'EN', 'site': 'Brain Pickings', 'tags': 'Culture'}
            new_values['title'] = right_side.find_all('a', class_="yellow")[i].contents[0]
            if len(right_side.find_all('a', class_="yellow")[i].contents) > 1:
                new_values['title'] = ''
                for j in right_side.find_all('a', class_="yellow")[i].contents:
                    try:
                        new_values['title'] += j
                    except:
                        new_values['title'] += j.contents[0]
            try:
                new_values['image'] = right_side.find_all('img', class_="wp-post-image")[1]['src']
            except:
                new_values['image'] = right_side.find_all('img')[1]['src']
            try:
                new_values['description'] = right_side.find_all('h2')[1].contents[0]
            except:
                new_values['description'] = ''
            new_values['url'] = right_side.find_all('a', class_="yellow")[i]['href']
            count += 1
            new_values['serial'] = str(count)
            archive_links.append(new_values)
    return len(archive_links)
pull_archive()

import json
with open('bp_dump1.json', 'w+') as f:
    json.dump(archive_links, f)