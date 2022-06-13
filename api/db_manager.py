from pprint import pprint as pp
import sqlite3
import random

publications = ['Aeon','Psyche','Fifty Two','Palladium',"fs blog","Alex Danco","Drew Devault","Margins","Ava","Seminar","Stratechery","Mark Manson",'The Marginalian',"Other"]

def read(count=1, source=None, link=None, short=None):
    con = sqlite3.connect('../buzo.db')
    cur = con.cursor()
    if link:
        # if link is defined (regardless of source)
        query = "SELECT * FROM articles WHERE url='" + link + "'"
        if short:
            query = "SELECT url,title,publication,excerpt,author,length FROM articles WHERE url='" + link + "'"
    else:
        # if both link and source are not defined
        # select a link at random but equal bias to all publications
        pub = random.sample(publications, k=1)[0]
        query = "SELECT DISTINCT url,title,publication,excerpt,author,length FROM articles ORDER BY RANDOM() LIMIT %s" % (str(count))
        # if source is defined
        if source:
            query = "SELECT url,title,publication,excerpt,author,length FROM articles WHERE publication='" + source + "' ORDER BY RANDOM() LIMIT " + str(count)
            if source == 'Favourites':
                query = "SELECT articles.url,title,articles.publication,excerpt,author,length FROM articles INNER JOIN links on articles.url = links.url WHERE links.Likes = 1"
    response = []

    for row in cur.execute(query):
        if link and not short:
            data = {
                'url': row[1],
                'title': row[2],
                'source': row[0],
                'excerpt': row[7],
                'author': row[3],
                'length': row[6],
                'html': row[4],
                'text': row[5]
            }
        else:
            data = {
                'url': row[0],
                'title': row[1],
                'source': row[2],
                'excerpt': row[3],
                'author': row[4],
                'length': row[5],
            }
        response.append(data)
    
    con.commit()
    con.close()
    pp(response)
    return response

def add(link):
    link = str(link)
    con = sqlite3.connect('../buzo.db')
    cur = con.cursor()
    # Check if the link exists in the Links table
    query = "SELECT * FROM links WHERE url='" + link + "'"
    response = []
    for row in cur.execute(query):
        response = row
    if response == []:
        cur.execute("INSERT INTO links VALUES (?,?,?,?)", (link,'Other',0,0))
        con.commit()
        con.close()
    return {'response':True}

def delete(link):
    con = sqlite3.connect('../buzo.db')
    cur = con.cursor()
    cur.execute("DELETE FROM links WHERE url=?", (link,))
    cur.execute("DELETE FROM articles WHERE url=?", (link,))
    con.commit()
    con.close()
    return {'response':True}

def update(link, likes):
    con = sqlite3.connect('../buzo.db')
    cur = con.cursor()
    cur.execute("UPDATE links SET Likes = ? WHERE url=?", (likes,link))
    con.commit()
    con.close()
    return {'response':True}