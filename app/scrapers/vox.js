// this file scrapes the entire Vox.com archive of articles
// and adds these properties to the links –
// featured-image: sailthru.image.full
// title: sailthru.title
// description: sailthru.description
// tags: sailthru.tags
// publication date: sailthru.date

years = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
months = [1,2,3,4,5,6,7,8,9,10,11,12]
years = [2014, 2015]


rootLink = "https://www.vox.com/archives/"
// require("openurl").open(rootLink)

for (var y=0; y < years.length; y++) {
    for (var m=0; m < months.length; m++) {
        var link = rootLink + years[y] + "/" + months[m]
    }
}


function loadAllLinks() {
    num_articles = document.getElementsByClassName('p-page-title')[0].innerHTML
    num_articles = parseInt(num_articles.match(/\(([0-9]*?)\)/)[1])
    if (num_articles % 30 === 0) { // (there are 30 results per page)
        num_pages = Math.floor(num_articles / 30) + 1 // trying one extra time than num pages
    } else {
        num_pages = Math.floor(num_articles / 30) + 2
    }

    for (var i=0; i < num_pages; i++) {
        loadMoreButton = document.getElementsByClassName('c-archives-load-more__button')
        loadMoreButton[0].click()
    }
}

function extractLinks() {
    z = document.getElementsByClassName('c-entry-box--compact__title')

    for (var i=0; i < z.length; i++) {
    l.push(z[i].firstChild.href)
    }
}

l = []

const Browser = require('zombie');
const browser = new Browser();
url = 'https://www.vox.com/archives/2020/7'
browser.visit(url, function() {
    loadAllLinks();
    extractLinks();
    console.log(l.length)
});