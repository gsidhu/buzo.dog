import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp 

# wrapper function
def scrape(html, parser, url):
    soup = BeautifulSoup(html, parser)
    if 'brainpickings' in url:
        soup = soup.find('div', class_="entry_content")
        p = soup.find_all(['h1','h2','h3','h4','h5','h6','p'])
    elif 'markmanson' in url:
        for unwanted in soup.find_all('div',{"class":['wp_rp_content','no-print', 'in-article-opt-in__inner']}):
            unwanted.decompose()
        # sometimes it is old school
        try:
            soup = soup.find('div', {'class':['post-content','entry-content']})
            p = soup.find_all(['h1','h2','h3','h4','h5','h6','p'])
        # other times it is semantic
        except:
            soup = soup.find('article')
            p = soup.find_all(['h1','h2','h3','h4','h5','h6','p'])
        try:
            fn = soup.find_all('span', id='fn-heading')
            fn.extend(soup.find_all('li', class_='fn-text'))
            p.extend(fn)
        except AttributeError:
            pass
    elif 'aeon' in url:
        soup = soup.find('div', class_='article__body__content')
        soup.find('div', class_='article__shares').decompose()
        p = soup.find_all(['h1','h2','h3','h4','h5','h6','p'])
    else:
        p = soup.find_all(['h1','h2','h3','h4','h5','h6','p'])

    endings = []
    for i in range(len(p)):
        try:
            endings.append(' '.join(p[i].get_text().split()[-3:]))
        except AttributeError:
            endings.append(p[i])

    value = []
    for k in range(len(p)):
        try:
            temp = p[k].get_text().replace('\\r\\n', ' ')
        except Exception as e:
            print(repr(e))
            temp = p[k].get_text()
        temp = ' '.join(temp.split())
        temp = temp.strip()
        value.append(temp)

    value = lists(value, soup, url)
    value = footnotes(value, soup)
    value = markdownify(value, soup, url)

    text = ''
    endices = []
    for k in range(len(value)):
        check = ' '.join(value[k].split()[-3:])
        if check in endings:
            if len(endices) == 0:
                text = ' '.join(value[:k+1])
            else:
                text = '\n'.join([text, ' '.join(value[endices[-1]+1:k+1])])
            endices.append(k)
    
    text = str('\n'.join([text, ' '.join(value[endices[-1]+1:])]))

    # Cleaning up
    for trash in ['donating = loving', 'Share\nFacebook', 'Like this:\nLike']:
        if trash in text:
            text = text[:text.find(trash)]

    text = superscripts(soup, text)
    text = tabulate(soup, text)

    # remove extra space in front of lines 
    # to keep list items correctly indented
    text = text.splitlines()
    for i in range(len(text)):
        try:
            # # remove double newline
            # if text[i] == '' and text[i-1] == '' :
            #     text.pop(i)
            #     continue
            # add newline but not to lists
            if not text[i][0] == '*' or text[i][0].isnumeric():
                text[i] = text[i] + '\n'
            text[i] = text[i].lstrip()
        except IndexError:
            # i don't know why
            pass
    text = '\n'.join(text)

    return text, value

def markdownify(value, soup, url):
    if 'india-seminar' in url:
        # Title
        if len(value[0]) > 0:
            value[0] = "## " + value[0] + "\n"
        # Author 
        if len(value[1]) > 0:
            value[1] = "#### " + value[1] + "\n"
    
    # Headings
    headings = soup.find_all(['h1','h2','h3','h4','h5','h6'])
    if len(headings) > 0:
        for h in headings:
            h = ' '.join(h.get_text().split())
            if h in value:
                value[value.index(h)] = "\n### " + h + "\n"

    return value

# lists
def lists(value, soup, url):
    ols = soup.find_all(['ol','ul'])
    # remove footnotes
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
