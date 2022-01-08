const playwright = require('playwright');
var { Readability } = require('@mozilla/readability');
var { JSDOM } = require('jsdom');
var sqlite3 = require('sqlite3');
// const fs = require('fs');

function createDatabase() {
  var newdb = new sqlite3.Database('buzo.db', (err) => {
    if (err) {
        console.log("Error: " + err);
        exit(1);
    }
    const query = `
      CREATE TABLE articles (
          publication varchar,
          url varchar,
          title varchar,
          author varchar,
          content varchar,
          textContent varchar,
          length int,
          excerpt varchar
      );
      `;
    newdb.exec(query);
  });
}

async function fetchData() {
  // fetch URL from DB
  var db = new sqlite3.Database("./buzo.db");
  db.all(`SELECT * FROM links WHERE Scraped = ? ORDER BY RANDOM() LIMIT 10;`, 0, async function(err, rows) {
    try {
      // connect browser
      browser = await playwright.chromium.launch({ headless: true });

      rows.forEach(async function (row) {
        if (checkExist(URL)) {
          return true
        }

        let response = await scrape(browser, row.URL, row.Publication)

        if (response) {
          addArticleToDB(response)
        }
      })
    } catch (err) {
      return console.log(err.message);
    } finally {
      // browser && await browser.close();
    }
  })
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
    else { console.log("Proceed") }
  })
}

function addArticleToDB(array) {
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

async function scrape(browser, URL, pub) {
  try {
    const page = await browser.newPage();

    // go to URL
    await page.goto(URL);
    await page.waitForLoadState();
    await page.waitForTimeout(500);

    // get source html
    var SOURCE = await page.content();

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

module.exports.fetchData = fetchData;
module.exports.flipBit = flipBit;