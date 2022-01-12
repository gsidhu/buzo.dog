import fs from 'fs';
import playwright from 'playwright';
let browser = await playwright.chromium.launch({ headless: false });
const page = await browser.newPage();

let result = ""

// let source = fs.readFileSync("/Users/thatgurjot/Downloads/ril_export.html", {encoding: "utf-8"}).toString();
// let url = 'https://www.india-seminar.com/2022/749.htm'
// for (var i=733; i < 749; i++) {
//     let url = ''
//     if (i < 737) {
//         url = 'https://www.india-seminar.com/2020/' + i + '.htm'
//     } else {
//         url = 'https://www.india-seminar.com/2021/' + i + '.htm'
//     }
//     pullLinks(url)
//     console.log(url)
// }

// let url = ''
// for (var i=1; i < 15; i++) {
//     url = 'https://palladiummag.com/page/' + i
//     await pullLinks(url)
//     console.log(url)
// }

let url = 'https://psyche.co/poiesis'
await page.goto(url)
await page.waitForLoadState();
let moreButton = '.byRteF'
for (var i=0; i < 15; i++) {
    console.log(i);
    await page.click(moreButton)
    await page.waitForTimeout(500)
}

const links = await page.$$('.fImuEk');
console.log(links.length);
for (const obj of links) {
    result = result + await obj.evaluate(element => element.href) + ",\n"
}

async function pullLinks(url) {
    await page.goto(url)
    await page.waitForLoadState();

    const links = await page.$$('.entry-permalink');
    for (const obj of links) {
        result = result + await obj.evaluate(element => element.href) + ",\n"
    }
}

fs.writeFile('new.txt', result, function (err) {
    if (err) return console.log(err);
});
await browser.close();