// Fixing mongo
// sudo lsof -iTCP -sTCP:LISTEN -n -P
// sudo kill <mongo_command_pid>
// sudo service mongod start

// guiding note 

**Backend:** Flask with MongoDB 
**Frontend**: Vue.js?

# Core
Websites are scraped and links are tagged and stored in the db. 
**Tags:** `source, timestamp, nsfw, `
db structure
    - core collection with all scraped links 
        - each document contains the link and its associated tag properties
    - collections for user data
        - each document stores the user's unique id, their preferences and any links they add

# Products
- Stand alone PWA / native app
- Bookmarklet (each user gets a unique URL with their preferences stored)
- Browser add-on

# Scrape sites
1. Pinboard 
    - /popular/
    - /popular/wikipedia
    - /t:psychology/
    - other tags scraped from the site
2. Reddit
    - front page
    - random
3. Awesome lists
4. Personal bookmarks

# UX / features
* Buttons to select sources
* Once preferences are set they can be saved in the local storage
    * or in db if account is made (read local storage for only 7 days to push account creation?)
* After this user just has to click 'Fetch'
* Option to 'fetch' anything at random or to 'browse' through a smaller selection

+ user can upload their personal bookmarks to the list
    + will only be accessible to them
    + or they can choose to add core db 
        + UI to allow selection which to add to core and which not
+ 

# Curation
- read site meta tags
    - get thumbnail 
    - language?
    - tags?
    - 

- True random vs preferred random
    - user can like/dislike sites
    - this preference could be for author/site, topic, content type (video/article/app), site load time


---------------------------------------------------------------------------

# Seminar 
* buzotext has all the text - GOOD 
* images need to be added at the right place 
* convert to markdown
  * first paragraph is title / h2 DONE
  * second is author / h4 DONE
  * headings are h3 or h4 DONE
  * footnotes: DONE
    * sup > [^1] DONE / REDO 
    * footnote number > [^1]: DONE / REDO
  * table > | __ |
  * img > {{< img class="center" data-src="a['href']" title="post title" alt="post title in issue name (#issue num, issue year)" >}} DONE
  * links > []() DONE
  * li > * DONE (won't work if non-unicode characters used)
  * blockquote > > DONE (won't work for nested blockquotes)
  * shortcodes for yt, vimeo, insta > done 
  * embedded tweets?


headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
            'From': 'buzo@buzo.dog'
        }
url = 'https://www.brainpickings.org/2013/03/04/amanda-palmer-on-the-art-of-asking-ted/'
r = requests.get(url, headers=headers)
t,v,s = scrape(r.content,'html5lib',url)
with open('./sas.txt','w+') as f:
    f.write(t)

## manual override
* http://www.india-seminar.com/2000/485/485%20index.htm

# text analysis 
- a lot more references being made in recent years than in past 
- word size and readability over the years 
- sentiment analysis 
- 