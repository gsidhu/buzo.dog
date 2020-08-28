# this file scrapes the entire Seminar archive of essays
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
    root_link = "http://www.india-seminar.com"
    year_root = "http://www.india-seminar.com/annual%20index/"
    count = 0
    for y in range(1999, 2021):
        if y < 2006:
            year_link = year_root + str(y) + '.htm'
        else:
            year_link = year_root + str(y) + '.html'
        
        r = requests.get(year_link)
        print('Looking at year ', str(y), '...', sep='')
        print('URL:', year_link)
        soup = BeautifulSoup(r.content, 'html.parser')

        for month in soup.find_all('tr'):
            try:
                month_name = ' '.join(month.find_all('a')[0].get_text().split()).strip()
                month_link = root_link + month.find_all('a')[0]['href'][2:]
                print('Looking at month ', str(month_name), '...', sep='')
                print('URL:', month_link)
                rr = requests.get(month_link)
            except:
                continue

            ssoup = BeautifulSoup(rr.content, 'html.parser')
            # extract issue information
            try:
                mid = ssoup.find('th')
            except Exception as e:
                print(repr(e))
            midtext = ' '.join(mid.get_text().split())
            
            for article in ssoup.find_all('li'):
                link = article.find('a')
                # this skips the edge case where the article has no link
                if type(link) == 'NoneType':
                    continue

                try:
                    new_values = {'language': 'EN', 'site': 'Seminar', 'tags': 'Social studies, Economy, Environment, Politics, Policy', 'year': str(y), 'issue_title': month_name, 'issue_num': link['href'][:3]}
                except:
                    continue

                # article information
                new_values['title'] = ' '.join(link.get_text().split()).title()
                try:
                    new_values['url'] = root_link + '/' + str(y) + '/' + link['href']
                except:
                    continue

                temp = ' '.join(article.get_text().split()).strip()
                if temp.lower() != new_values['title']:
                    new_values['author'] = temp[temp.lower().find(new_values['title'].lower())+len(new_values['title'])+1:]

                # issue information
                new_values['description'] = midtext[midtext.find('a sym'):midtext.find('cover')].strip().title()
                new_values['image'] = root_link + mid.find('img')['src'][2:]
                new_values['image_credits'] = midtext[midtext.find('cover'):].strip().title()

                count += 1
                new_values['serial'] = str(count)
                archive_links.append(new_values)
    return len(archive_links)
pull_archive()

import json
with open('seminar_dump.json', 'w+') as f:
    json.dump(archive_links, f)