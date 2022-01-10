import playwright from 'playwright';
import fs from 'fs';
import { Readability } from '@mozilla/readability';
import { JSDOM } from 'jsdom';
import sqlite3 from 'sqlite3';
import scrape from 'website-scraper';
import SaveToExistingDirectoryPlugin from 'website-scraper-existing-directory';

const scrapeOptions = {
  urls: [],
  directory: './local',
  sources: [ {selector: 'html'} ],
  plugins: [ new SaveToExistingDirectoryPlugin() ]
};

function fetchData() {
  // fetch URL from DB
  var db = new sqlite3.Database("./buzo.db");
  db.all(`SELECT * FROM links WHERE Scraped = 0 ORDER BY RANDOM() LIMIT 1000;`, async function(err, rows) {
    try {
      for (var i=0; i < rows.length; i++) {
        let row = rows[i]
        // check if link already exists in articles table
        if (checkExist(row['URL'])) {
          continue
        }
        // download page source
        try {
          scrapeOptions['urls'] = [row['URL']]
          await scrape(scrapeOptions);
          let source = getSource();
          let response = readSource(source, row.URL, row.Publication)
          if (response) {
            addArticleToDB(response)
          } else {
            continue
          }
        } catch(err) {
          // console.log(err.message)
          // console.log(row['URL'])
          // console.log("Switching to headless")
          try {
            let source = await getHeadlessSource(row['URL'])
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
  await page.goto(URL);
  await page.waitForLoadState();
  await page.waitForTimeout(1000);

  // get source html
  var SOURCE = await page.content();
  
  await browser.close();
  return SOURCE
}

async function getSource() {
  // get source html
  let SOURCE = fs.readFileSync("./local/index.html", {encoding: "utf-8"}).toString();
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

function addArticleToDB(array) {
  // don't add if the array is not proper
  if (array[2] === '' | array[6] < 200) {
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

flipBit()
fetchData()
