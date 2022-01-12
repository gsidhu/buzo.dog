import sqlite3 from 'sqlite3';
import fs from 'fs';

function addLinksToDB() {
    // load links JSON
    fs.readFile('./linksdb.json', 'utf8', (err, data) => {
        if (err) {
            console.log(`Error reading file from disk: ${err}`);
        } else {
            let poo = 0
            // parse JSON string to JSON object
            const links = JSON.parse(data);

            // add to db
            var db = new sqlite3.Database("./buzo.db");
            for (const pub of Object.keys(links)) {
                let numLinks = links[pub].length
                for (var i=0; i < numLinks; i++) {
                    let l = links[pub][i]
                    // check if already exists in db
                    db.all(`SELECT URL FROM links WHERE URL = ?`, l, function(err, rows) {
                        if (err) {
                          return console.log(err.message);
                        }
                        if (rows.length === 0) {
                            let array = [l, pub, 0, 0]
                            db.run(`INSERT INTO links(URL, Publication, Scraped, Likes) VALUES(?,?,?,?)`, array, function(err) {
                                if (err) {
                                    return console.log(err.message);
                                }
                                // get the last insert id
                                console.log(`A row has been inserted with rowid ${this.lastID}`);
                            });
                        } else {
                            // console.log("Link already exists in DB")
                        }
                    });
                }
            }
        }
    });
}

addLinksToDB()