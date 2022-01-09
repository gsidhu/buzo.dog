import playwright from 'playwright';
let browser = await playwright.chromium.launch({ headless: true });
const page = await browser.newPage();

// go to URL
await page.goto('http://whatsmyuseragent.org/');
await page.waitForLoadState();
await page.waitForTimeout(1000);

let q = await page.content()
console.log(q)
await browser.close();