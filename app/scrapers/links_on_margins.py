# this file scrapes links from Links on the Margins posts
# and adds these properties to the links –
# featured-image:  wp-post-image img
# title: sailthru.title
# description: article-card__standfirst
# tags: article-card__topic
# publication date: sailthru.date

# import requests
# from bs4 import BeautifulSoup
# from pprint import pprint as pp

# import metadata_parser

archive_links = []
def pull_archive():
    count = 0
    with open('/Users/thatgurjot/Git Repos/buzo.dog/app/scrapers/margins.html', 'r+') as f:
        r = f.read()
    soup = BeautifulSoup(r, 'html.parser')
    links = soup.find_all('a', class_="post-preview-description")

    for c in range(len(links)):
        if c%2 == 0:
            continue
        rr = requests.get(links[c]['href'])
        ss = BeautifulSoup(rr.content, 'html.parser')
        ll = ss.find_all('h3')
        inner_count = 1
        for cc in ll:
            z = cc.find('a')
            if inner_count:
                inner_count = 0
                continue
            new_values = {'language': 'EN', 'site': 'Margins', 
                        'tags': 'Opinion', 'image': 'https://cdn.substack.com/image/fetch/w_96,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F6fc17be7-df3b-43ce-b8c2-4388c0a27d1f_250x250.png'}

            try:
                new_values['title'] = z.contents[0]
            except:
                continue
            try:
                new_values['url'] = z['href']
            except:
                continue
            try:
                new_values['description'] = cc.find_next('p').find('em').contents[0]
            except:
                new_values['description'] = ''

            count += 1
            new_values['serial'] = str(count)
            archive_links.append(new_values)
    return len(archive_links)
pull_archive()

import json
with open('links_on_margins_dump.json', 'w+') as f:
    json.dump(archive_links, f)