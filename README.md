# buzo.xyz
A no nonsense internet explorer.

## About
### What is this site?
buzo.xyz is a no nonsense internet explorer. The internet has all sorts of beautiful weirdness to it. Buzo helps you explore it.

### What can I do here?
A couple of things. You can 'Fetch' a cool link, or you can go for a 'Walk' and decide which link to follow. Buzo will be with you through it all, in spirit.

### This is a cool site. Can I help?
Sure! You can help me cover the cost of keeping this site up and for buying Buzo treats. (belly rubs cost extra) Head over to the Sponsor links in this repository to donate.

### What features are in the pipeline?
A bunch -
1. Publication Reader: Kind of like an RSS reader but for reading best-of archives instead of the latest
2. Categorised Viewing: Looking for comics, articles, news, cool sites? We got them
3. User Profiles: Upload your bookmarks, share them across devices, maintain your personal reading lists (read, to-read) - all in a secure and private environment; no login, no data shared with anyone

### Terms and Conditions
buzo.xyz is shared under a CC-BY-SA-4.0 license. The creators of this site are not liable for any content that you may access through this site. The creators claim no ownership over the content aggregated, displayed and accessed through this site. By using this site you are implicitly agreeing to these terms and conditions.

## Development
### Basic Architecture
The site exists in two parts -
1. **A Flask API.** See `./app/`.
2. **A VueJS front-end.** See `./buzo.xyz/`.

### Configuring local environment
To configure virtual environment on your machine –

1. Install Python 3 from [Python.org](https://www.python.org/downloads/). Comes pre-installed if you're using a modern UNIX-based OS.
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
*Rest of the instructions coming soon...*