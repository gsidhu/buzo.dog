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

# import metadata_parser

archive_links = []
def pull_archive():
    root_link = "https://alexdanco.com/page"
    count = 0
    for d in range(1,19):
        l = root_link + "/" + str(d) + "/"
        print('Looking at page ', str(d), '...', sep='')
        print('URL:', l)
        r = requests.get(l)
        soup = BeautifulSoup(r.content, 'html.parser')

        for link in soup.find_all('article', class_="post"):
            new_values = {'language': 'EN', 'site': 'Alex Danco\'s Newsletter', 'tags': 'Tech, Economy, Opinion'}

            new_values['title'] = link.find_all('h2', class_="entry-title")[0].find('a').contents[0]

            try:
                new_values['image'] = link.find_all('a', class_='thumbnail')[0].find_all('img')[0]['src']
            except:
                new_values['image'] = ''
            
            try:
                new_values['description'] = link.find_all('p')[0].contents[0].strip()
            except:
                new_values['description'] = ''
                continue

            new_values['url'] = link.find_all('h2', class_="entry-title")[0].find('a')['href']
            
            count += 1
            new_values['serial'] = str(count)
            archive_links.append(new_values)
    return len(archive_links)
pull_archive()

import json
with open('alexdanco_dump.json', 'w+') as f:
    json.dump(archive_links, f)