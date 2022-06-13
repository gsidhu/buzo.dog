import fs from 'fs';
import playwright from 'playwright';
let browser = await playwright.chromium.launch({ headless: true });
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
// let url = 'https://bigthink.com/neuropsych'
// await page.goto(url)
// await page.waitForLoadState();
// let moreButton = '.byRteF'
// for (var i=0; i < 15; i++) {
//     console.log(i);
//     await page.click(moreButton)
//     await page.waitForTimeout(500)
// }
// const links = await page.$$('.fImuEk');
// console.log(links.length);
// for (const obj of links) {
//     result = result + await obj.evaluate(element => element.href) + ",\n"
// }

for (var i=1; i < 37; i++) {
    let url = 'https://bigthink.com/neuropsych?paging=' + i
    await pullLinks(url)
    console.log(url)
}

async function pullLinks(url) {
    await page.goto(url)
    await page.waitForLoadState();

    const links = await page.$$('.card-headline a');
    for (const obj of links) {
        result = result + await obj.evaluate(element => element.href) + ",\n"
    }
}

fs.writeFile('new.txt', result, function (err) {
    if (err) return console.log(err);
});

await browser.close();