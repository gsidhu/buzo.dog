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
    - 