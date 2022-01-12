// This script checks for new links in the DB and fetches their articles
// It runs on a cronjob twice a day

import playwright from 'playwright';
import { Readability } from '@mozilla/readability';
import { JSDOM } from 'jsdom';
import sqlite3 from 'sqlite3';

function fetchData() {
  // fetch URL from DB
  var db = new sqlite3.Database("./buzo.db");
  db.all(`SELECT * FROM links WHERE Scraped = 0`, async function(err, rows) {
    try {
      if (rows.length === 0) { console.log("No new links."); }
      for (var i=0; i < rows.length; i++) {
        let row = rows[i]
        // check if link already exists in articles table
        if (checkExist(row['URL'])) {
          continue
        }
        // download page source
        try {
          let source = await getHeadlessSource(row['URL'])
          if (source === "skip") { continue }
          let response = readSource(source, row.URL, row.Publication)
          if (response) {
            addArticleToDB(response)
          } else {
            continue
          }
        } catch (err) {
          console.log(err.message);
        } finally {
          // browser && await browser.close();
        }
      }
    } catch (err) {
      return console.log(err.message);
    } finally {
      flipBit()
    }
  })
}
  
async function getHeadlessSource(URL) {
  // connect browser
  const browser = await playwright.chromium.launch({ headless: true });
  const page = await browser.newPage();

  // go to URL
  try {
    await page.goto(URL, {timeout: 5000 });
    // get source html
    var SOURCE = await page.content();
  } catch (error) {
    console.log(error.message)
    SOURCE = "skip"
    markBadLink(URL)
  } finally {
    await browser.close();
  }
  return SOURCE
}
  
function readSource(SOURCE, URL, pub) {
  try {
    const dom = new JSDOM(SOURCE, {
      url: URL,
      contentType: "text/html",
    });

    // extract article from source
    let reader = new Readability(dom.window.document);
    let article = reader.parse();

    article["url"] = URL;
    article["publication"] = pub;
    let array = [article['publication'], article['url'], article['title'], article['byline'], article['content'], article['textContent'], article['length'], article['excerpt']];

    return array;
  } catch (e) {
    console.log(e.message);
    return false;
  }
}

function addArticleToDB(array) {
  // don't add if the array is not proper
  if (array[2] === '' | array[6] < 200) {
    console.log("Bad fetch. Skipping.");
    markBadLink(array[1])
    return
  }

  var db = new sqlite3.Database("./buzo.db");
  // insert article to db
  db.run(`INSERT INTO articles(publication, url, title, author, content, textContent, length, excerpt) VALUES(?,?,?,?,?,?,?,?)`, array, function(err) {
    if (err) {
      console.log(err.message);
      return false
    }
    // get the last insert id
    console.log(`A row has been inserted with rowid ${this.lastID}`);
    return true
  });
}

function flipBit() {
  var db = new sqlite3.Database("./buzo.db");
  // flip the bit
  db.run(`UPDATE links SET Scraped = 1 WHERE url in (SELECT links.url FROM links INNER JOIN articles ON articles.url = links.URL WHERE links.Scraped = 0)`, function(err) {
    if (err) {
      console.log(err.message);
      return false
    }
    console.log("Bits flipped")
    return true
  });
}

function checkExist(URL) {
  var db = new sqlite3.Database("./buzo.db");
  // check if link already exists in db
  db.all(`SELECT url FROM articles WHERE url = ?`, URL, function(err, rows) {
    if (err) {
      return console.log(err.message);
    }
    // quit process if exists
    if (rows.length != 0) { return true }
    // else { console.log("Proceed") }
  })
}

function markBadLink(URL) {
  var db = new sqlite3.Database("./buzo.db");
  // check if link already exists in db
  db.all(`UPDATE links SET publication = 'Bad' WHERE url = ?`, URL, function(err, rows) {
    if (err) {
      return console.log(err.message);
    }
    return true
  })
}


flipBit()
fetchData()