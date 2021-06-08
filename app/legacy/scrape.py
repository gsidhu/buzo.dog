import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp 

try:
    from . import sources
except:
    import sources

import wikipedia

import praw
from praw.models import MoreComments
import re

reddit = praw.Reddit(client_id="1oXk1bgCT1Zf7A",
                    client_secret="3xj4c0XzzbeyzwGGrtCyk8rUqfI",
                    user_agent="buzo.xyz by u/justcantgradschool",
                    username='justcantgradschool',
                    password='drowssap4321')

def reddit_url_extracter(l):
    links = []
    submission = reddit.submission(l)
    # all_comments = submission.comments.list()
    for top_comment in submission.comments:
        if isinstance(top_comment, MoreComments):
            continue
        body = top_comment.body
        url = ''
        ## works for only one url per comment
        # detect url markdown 
        temp = re.findall('\[.*?\)',body)
        for s in temp:
            # if a link exists in the comment, extract url
            url = s[s.find("(")+1:s.find(")")]
            links.append(url.lower())
        
        if url == '':
            # look for all http(s) links in comments
            temp = re.findall('\(http(.*?)\s', body)
            for s in temp:
                url = s[s.find("(")+1:s.find(")")]
                links.append(url.lower())
    return links

def reddit_subreddit_url_extracter(sub, sort='top', by='all'):
    links = []
    if sort == 'top':
        for submission in reddit.subreddit(sub).top(by):
            if not submission.over_18:
                links.append(submission.url)
        for submission in reddit.subreddit(sub).top('month'):
            if not submission.over_18:
                links.append(submission.url)
    return links

def pinboard_load():
    links = []
    for l in sources.regular_scraps:
        r = requests.get(l)
        soup = BeautifulSoup(r.content, 'html.parser')

        for link in soup.find_all('a', class_="bookmark_title"):
            links.append(link.get('href'))
    return links

def wikiscraper():
    r = wikipedia.random(10)
    for i in r:
        p = wikipedia.page(title=i)
        # print(i, len(p.content.split(' ')))
        print(i, len(p.summary.split(' ')))
