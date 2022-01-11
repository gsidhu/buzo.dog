# buzo.xyz
A personal archive.

## About
### What is this site?
buzo.xyz is a personal archive. It is a library of articles from a selection of publications spanning across culture, technology, science, philosophy and general wisdom. This website has emerged out of my desire to teach myself the fundamentals of web development with Vuejs. And now Node JS and SQL as well.

### What can I do here?
A couple of things. You can 'Fetch' a cool link, or you can go for a 'Walk' and decide which link to follow. Buzo will be with you through it all, in spirit.

### This is a cool site. Can I help?
Sure! You can help me cover the cost of keeping this site up and for buying Buzo treats. (belly rubs cost extra) Head over to the Sponsor links in this repository to donate.

### What features are in the pipeline?
Definitely -
* **Standalone scraper:** Enter a link and if it's not paywalled, Buzo will scrape its text for you and you can download it as .html, .txt, .md, .docx or .pdf

Likely -
* **Search:** Put in some keywords and it'll find articles that have them
* **Filter:** Mark certain publications or keywords that you don't want to show on the feed

Unlikely -
* **User profiles:** Upload your bookmarks, share them across devices, maintain your personal reading lists (read, to-read) - all in a secure and private environment; no login, no data shared with anyone

### Terms and Conditions
buzo.xyz is shared under a CC-BY-SA-4.0 license. The creators of this site are not liable for any content that you may access through this site. The creators claim no ownership over the content aggregated, displayed and accessed through this site. By using this site you are implicitly agreeing to these terms and conditions.

## Development

### Basic Architecture
The site exists in multiple parts -
1. **A Fast API.** See `./api/`.
2. **A VueJS front-end.** See `./buzo.xyz/`.
3. **A Node JS scraper.** See `work.js`.
4. **A SQLite database.**

### Configuring local environment
To configure virtual environment on your machine –

1. Install Python 3 from [Python.org](https://www.python.org/downloads/). Comes pre-installed if you're using a modern UNIX-based OS. You'll need Python 3.9 for Fast API's `uvloop` dependency.
2. [Download this repository](https://github.com/gsidhu/buzo.xyz/archive/master.zip).
3. Open a Terminal window and point it to the root of this directory.
4. To create a virtual environment called `venv`, run –
```
python3 -m venv venv
```
5. Activate the virtual environment using –
```
source venv/bin/activate
```
6. Inside the virtual environment, install all dependencies by running -
```
pip install -r requirements.txt
```

Everything you do to the Python code should happen inside of this virtual environment because that's where your dependencies are installed. So make sure to activate it each time. You should see `(venv)` in front of your username in the Terminal window when it is activated.

### Code logic
1. Links in the `linksdb.json` are added to the database through `addLinks.js`.
2. The script in `work.js` fetches articles for all the links in the database, incremently.
3. The API acts as the middle layer, responding to the queries coming from the front-end.