# this file scrapes the entire fs.blog archive of essays
# and adds these properties to the links –
# featured-image: <figure style url bg image>
# title: sailthru.title
# description: article-card__standfirst
# tags: article-card__topic
# publication date: sailthru.date

import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp

archive_links = []
def pull_archive(category, pages):
    root_link = "https://fs.blog/category/" + str(category) + "/page/"
    count = 0
    for d in range(1,pages+1):
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
        for link in soup.find_all('article'):
            new_values = {'language': 'EN', 'site': 'fs blog', 
            'image': 'https://149366099.v2.pressablecdn.com/wp-content/uploads/2020/06/FS-LOGO.png', 'tags': 'Thinking, Writing, Learning'}

            new_values['title'] = str(link.find('h2').find('a').contents[0])
            new_values['url'] = str(link.find('h2').find('a')['href'])
            
            try:
                new_values['description'] = str(link.find('p').contents[0])
                if '<em>' in new_values['description']:
                    new_values['description'] = str(link.find('p').find('em').contents[0])
            except:
                new_values['description'] = ''
            inner_count += 1
            count += 1
            new_values['serial'] = str(count)
            archive_links.append(new_values)
    file_name = 'fsblog_' + category + '_dump.json'
    with open(file_name, 'w+') as f:
        json.dump(archive_links, f)
    return len(archive_links)

cats = ['thinking', 'writing', 'decision-making', 'culture', 'mental-models', 'uncategorized', 'science']
nums = [22, 4, 16, 9, 20, 22, 9]
for i in range(len(cats)):
    pull_archive(cats[i], nums[i])