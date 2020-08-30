import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp 

# wrapper function
def scrape(html, parser, url):
    soup = BeautifulSoup(html, parser)
    # kill nav
    # soup.find('nav').decompose()
    if 'brainpickings' in url:
        soup = soup.find('div', class_="entry_content")
    elif 'markmanson' in url:
        for unwanted in soup.find_all('div',{"class":['wp_rp_content','no-print', 'in-article-opt-in__inner']}):
            unwanted.decompose()
        # sometimes it is old school
        try:
            soup = soup.find('div', {'class':['post-content','entry-content']})
        # other times it is semantic
        except:
            soup = soup.find('article')
        try:
            # add footnotes
            fn = soup.find_all('span', id='fn-heading')
            fn.extend(soup.find_all('li', class_='fn-text'))
        except AttributeError:
            pass
    elif 'aeon' in url:
        soup = soup.find('div', class_='article__body__content')
        soup.find('div', class_='article__shares').decompose()
    
    # markdownify
    strungsoup = str(soup)
    strungsoup = markdownify(soup, strungsoup)
    value = lists(value, soup, url)
    value = footnotes(value, soup)
    value = headings(value, soup, url)
    value = superscripts(value, soup)
    value = links(value,soup)

    soup = BeautifulSoup(strungsoup, 'html5lib')

    p = soup.find_all(['h1','h2','h3','h4','h5','h6','p'])

    # add markmanson footnotes
    if 'markmanson' in url:
        p.extend(fn)
    return text, value, soup

# markdownify
def markdownify(soup, strungsoup):
    # italics
    for st in soup.find_all(['em']):
        replacement_text = "_" + str(st) + "_"
        strungsoup = strungsoup.replace(str(st), replacement_text)
    # strike
    for st in soup.find_all('strike'):
        replacement_text = "~~" + str(st) + "~~"
        strungsoup = strungsoup.replace(str(st), replacement_text)
    # bold
    for st in soup.find_all('b'):
        replacement_text = "*" + str(st) + "*"
        strungsoup = strungsoup.replace(str(st), replacement_text)
    # blockquotes 
    bqs = soup.find_all('blockquote')
    covered = []
    for bq in bqs:
        if str(bq) in covered:
            continue
        bqtext = ''
        for b in bq.children:
            if str(b) != '\n':
                bqtext += ">" + str(b) + "\n"
        replacement_text = '<blockquote>' + bqtext + '</blockquote>'
        strungsoup = strungsoup.replace(str(bq), replacement_text)
    # headings
    headings = soup.find_all(['h1','h2','h3','h4','h5','h6'])
    for h in headings:
        htext = '###' + h.get_text()
        h = ' '.join(h.get_text().split())
        if h in value:
            value[value.index(h)] = "\n### " + h + "\n"
    return strungsoup

# links
def links(text, soup):
    all_links = soup.find_all('a')
    covered = []
    for link in all_links:
        # looks at the parent tag, turns html into md into html into text
        # then switches the text in the buzotext
        parent = link.parent
        # cop out if already covered in sister tag
        if parent in covered:
            continue

        covered.append(parent)
        otext = parent.get_text()

        lindex = text.find(otext)
        try:
            if lindex == -1:
                lindex = text.encode('utf-8').find(otext.encode('utf-8'))
            if lindex == -1:
                continue
        except:
            continue
        findex = lindex + len(otext)
        
        child_links = parent.find_all('a')
        ltext = otext
        clash = {}
        for cl in child_links:
            clraw = str(cl)
            clmd = "[" + cl.get_text() + "](" + cl['href'] + ")"
            clash[clraw] = clmd

        for clraw in clash.keys():
            parent = str(parent).replace(clraw, clash[clraw])
        ltext = BeautifulSoup(parent).get_text()

        try:
            text = text[:lindex] + ltext + text[findex:]
        except:
            continue
    return text

# headings
def headings(value, soup, url):
    if 'india-seminar' in url:
        # Title
        if len(value[0]) > 0:
            value[0] = "## " + value[0] + "\n"
        # Author 
        if len(value[1]) > 0:
            value[1] = "#### " + value[1] + "\n"

    return value

# lists
def lists(value, soup, url):
    ols = soup.find_all(['ol','ul'])
    if len(ols) == 0:
        return value
    for l in ols:
        if 'markmanson' in url:
            if 'Footnotes' in ' '.join(l.find_previous('span').get_text().split()):
                ols.remove(l)
                continue
        mdli = []
        count = 0
        for i in l.find_all('li'):
            count += 1
            if i.find_parent().name == 'ol':
                line = str(count) + '. ' + ' '.join(i.get_text().split())
            elif i.find_parent().name == 'ul':
                line = "* " + ' '.join(i.get_text().split())
            
            if count == (len(l.find_all('li'))):
                line +=  '\n\n'
            else:
                line +=  '\n'
            mdli.append(line.lstrip())
        # find insert index from last <li> element
        tracer = ' '.join(i.find_previous(['p','h5','h4','h3','h2','h1','span','div']).get_text().split())
        try:
            lindex = value.index(tracer)
            value = value[:lindex+1] + mdli + value[lindex+1:]
        except IndexError:
            pass
    return value

# footnotes - bottom link
def footnotes(value, soup):
    sups = soup.find_all('sup') # footnotes are all superscript
    for sup in sups:
        if not sup.get_text().isnumeric():
            sups.remove(sup)
    if 'Footnotes:' in value:
        findex = value.index('Footnotes:')
    elif 'Footnotes' in value:
        findex = value.index('Footnotes')
    else:
        return value
    for i in range(len(sups)):
        if value[findex+i+1][0] != sups[i].get_text()[0]:
            value[findex+i+1] = "[^" + sups[i].get_text() + "]:" + sups[i].get_text() + ". " + value[findex+i+1][len(sups[i].get_text())-1:] + '\n'
        else:
            value[findex+i+1] = "[^" + sups[i].get_text() + "]:" + value[findex+i+1][len(sups[i].get_text())-1:]  + '\n'
        if '↵' in value[findex+i+1]:
            value[findex+i+1] = value[findex+i+1].replace('↵','')
    return value
 
# footnotes - superscript
def superscripts(soup, text):
    sups = soup.find_all('sup') # footnotes are all superscript
    for sup in sups:
        check = sup.find_previous()
        while str(sup) not in str(check) or len(check.get_text()) <= len(sup.get_text()):
            check = check.find_previous()
        check = BeautifulSoup(str(check)[:str(check).find(str(sup))])
        place = ' '.join(check.get_text().split()[-3:])
        if check.get_text()[-1] == ' ':
            tracer = place + ' ' + sup.get_text()
        else:
            tracer = place + sup.get_text()
        sindex = text.find(tracer)

        if sindex > -1:
            replacement = place + "[^" + sup.get_text() + "]"
            text = text[:sindex] + replacement + text[sindex+len(tracer):]

    return text

# tables html
def tabulate(soup, text):
    # turns the tables in the text into html tables
    tables = soup.find_all('table')
    if len(tables) == 0:
        return text
    lines = text.split('\n')
    for tb in tables:
        rows = tb.find_all('tr')
        ncols = [len(tr.find_all('td')) for tr in rows]
        htable = '''<table class='table table-bordered'><tbody>'''
        for n in range(len(rows)):
            htable += "<tr>"
            for c in range(ncols[n]):
                if ncols[n] == 1:
                    htable += "<td colspan=" + str(max(ncols)) + "'>"
                else:
                    htable += '<td>'
                htable += ' '.join(rows[n].find_all('td')[c].get_text().replace('\n', '').split())
                htable += '</td>'
                if n == 0:
                    first = ' '.join(rows[n].find_all('td')[c].get_text().replace('\n', '').split())
                if n == (len(rows)-1):
                    last = ' '.join(rows[n].find_all('td')[c].get_text().replace('\n', '').split())
            htable += "</tr>"
        htable += '''</tbody></table>'''
    
        try:
            findex = lines.index(first)
        except ValueError:
            for j in range(1,len(first.split())+1):
                if ' '.join(first.split()[:j]) in lines:
                    findex = lines.index(' '.join(first.split()[:j]))
                    break
        
        try:
            lindex = lines.index(last)
        except ValueError:
            for j in range(1,len(last.split())+1):
                if ' '.join(last.split()[:j]) in lines:
                    lindex = lines.index(' '.join(last.split()[:j]))
                    break
        
        lines = lines[:findex] + [htable] + lines[lindex+1:]
    
    text = '\n'.join(lines)
    return text

headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
            'From': 'buzo@buzo.dog'
        }
url = 'https://www.brainpickings.org/2013/08/02/frida-kahlos-politics/'
r = requests.get(url, headers=headers)
t,v,s = scrape(r.content,'html5lib',url)
with open('./sas.txt','w+') as f:
    f.write(t)

# 'Through the very act of asking people, I connected with them. And when you connect with them, people want to help you. It’s kind of counterintuitive for a lot of artists — they don’t want to ask for things. It’s not easy to ask. … Asking makes you vulnerable.' in s

# q = bquotes(s,v)
# pp(q[2:8])

# v[-10:]

# q = bquotes(v,s)
# q[-10:]

# q = strike(t,s)
# with open('./sas.txt','w+') as f:
#     f.write(q)