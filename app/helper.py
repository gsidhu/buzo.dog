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
            fn = soup.find_all('span', id='fn-heading')
            fn.extend(soup.find_all('li', class_='fn-text'))
        except AttributeError:
            pass
    elif 'aeon' in url:
        soup = soup.find('div', class_='article__body__content')
        soup.find('div', class_='article__shares').decompose()
    elif 'margins.substack' in url:
        soup = soup.find('div', class_='body')
        # soup.find_all('div', class_='tweet').decompose()

    strungsoup = str(soup)
    strungsoup = images(soup, strungsoup)
    strungsoup = shortcodes(soup, strungsoup)
    strungsoup = strikeembold(soup, strungsoup)
    soup = BeautifulSoup(strungsoup, 'html5lib')

    p = soup.find_all(['h1','h2','h3','h4','h5','h6','p','buzo'])

    # add markmanson footnotes
    if 'markmanson' in url:
        p.extend(fn)

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
    
    value = bquotes(value, soup)
    value = lists(value, soup, url)
    value = footnotes(value, soup)
    value = headings(value, soup, url)

    # remove duplicate elements 
    # these are usually caused by the buzo-span tags
    value = list(dict.fromkeys(value))
    
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
    # remove double image / happens in brainpickings
    if text[1] in text[0]:
        text.pop(1)
    for i in range(len(text)):
        try:
            # add newline but not to lists or blockquotes
            if not (text[i][0] == '*' or text[i][0].isnumeric() or text[i][0] == '>'):
                text[i] = text[i] + '\n'
            text[i] = text[i].lstrip()

        except IndexError:
            # i don't know why
            pass
    text = '\n'.join(text)

    # blockquote edge cases
    if ">[…]" in text:
        text.replace(">[…]", ">[…]\n")
    text = text.replace('\n>', '  \n>')
    text = text.replace('>\n', '>\n>')
    text = text.replace('\n  \n>','  \n>  ')

    text = links(text,soup)

    return text, value, soup

# strikethrough, italics and bold
def strikeembold(soup, strungsoup):
    for st in soup.find_all(['em','strike','b','strong']):
        key = str(st)
        # italics
        if st.name == 'em':
            replacement_text = str(st).replace('<em>','_')
            replacement_text = replacement_text.replace('</em>','_')
            replacement_text = replacement_text.replace(' _', '_')
            replacement_text = replacement_text.replace('_ ', '_')
            if key in strungsoup:
                strungsoup = strungsoup.replace(key, replacement_text)
        # strike
        if st.name == 'strike':
            replacement_text = str(st).replace('<strike>','~~')
            replacement_text = replacement_text.replace('</strike>','~~')
            replacement_text = replacement_text.replace(' ~~', '~~')
            replacement_text = replacement_text.replace('~~ ', '~~')
            if key in strungsoup:
                strungsoup = strungsoup.replace(key, replacement_text)
        # bold
        if st.name in ['b','strong']:
            replacement_text = str(st).replace(('<'+st.name+'>'),'__')
            replacement_text = replacement_text.replace(('</'+st.name+'>'),'__')
            replacement_text = replacement_text.replace(' __', '__')
            replacement_text = replacement_text.replace('__ ', '__')
            if key in strungsoup:
                strungsoup = strungsoup.replace(key, replacement_text)
    return strungsoup

# blockquotes
def bquotes(value, soup):
    bqs = soup.find_all('blockquote')
    for bq in bqs:
        ps = bq.find_all('p')
        for p in range(len(ps)):
            if ps[p].find('br'):
                replacement = str(ps[p]).replace('<br/>','<br/>\n>')
                replacement = BeautifulSoup(replacement,'html5lib').get_text()
            else:
                replacement = ps[p].get_text()
            pindex = value.index(ps[p].get_text().strip().replace('\n',' '))
            if p == (len(ps)-1):
                value[pindex] = ">" + replacement + "\n"
            else:
                value[pindex] = ">" + replacement
    return value

# images
def images(soup, strungsoup):
    all_images = soup.find_all('img')
    for im in all_images:
        vals = {'src': '', 'title': '', 'alt': '', 'caption':''}
        if 'data:' in im['src']:
            continue
        if im.next.name == 'figcaption':
            try:
                im.next.find('br').replace_with('\n')
            except AttributeError:
                pass
            vals['caption'] = im.next.text
        vals['src'] = im['src']
        if 'title' in im.attrs.keys():
            vals['title'] = im['title']
        if 'alt' in im.attrs.keys():
            vals['alt'] = im['alt']
        # add p tags so it gets picked up by buzo
        mdimg = '''<buzo class='buzo'>{{< img class="center" data-src="%s" title="%s" alt="%s" caption="%s">}}</buzo>''' % (vals['src'], vals['title'], vals['alt'], vals['caption'])
        strungsoup = strungsoup.replace(str(im), mdimg)
    return strungsoup

# youtube, vimeo, instagram, twitter
def shortcodes(soup, strungsoup):
    all_links = soup.find_all(['a', 'iframe'])
    for link in all_links:
        check = str(link)
        md = ''
        if 'youtu.be' in check or 'www.youtube.com' in check or 'youtube-nocookie.com' in check:
            if check.find('watch?v=') > -1:
                yt_id = check[check.find('watch?v=')+8:check.find('watch?v=')+8+11]
            elif check.find('youtube.com/embed/') > -1:
                yt_id = check[check.find('youtube.com/embed/')+18:check.find('youtube.com/embed/')+18+11]
            elif check.find('youtube-nocookie.com/embed/') > -1:
                yt_id = check[check.find('youtube-nocookie.com/embed/')+27:check.find('youtube-nocookie.com/embed/')+27+11]
            # add p tags so it gets picked up by buzo
            md = '''<buzo class='buzo'>{{< youtube %s>}}</buzo>''' % (yt_id)
        if '://vimeo.com/' in check:
            vimeo_id = check[check.find('://vimeo.com/')+13:check.find('://vimeo.com')+13+8]
            md = '''<buzo class='buzo'>{{< vimeo %s>}}</buzo>''' % (vimeo_id)
        if '://twitter.com' in check:
            if check.find('/status/') > -1 and link.text == link['href']:
                tweet_id = check[check.find('/status/')+8:check.find('/status/')+8+19]
                md = '''<buzo class='buzo'>{{< twitter %s>}}</buzo>''' % (tweet_id)
        if '://instagram.com/p/' in check:
            insta_id = check[check.find('instagram.com/p/')+8:check.find('instagram.com/p/')+16+11]
            md = '''<buzo class='buzo'>{{< instagram_simple %s hidecaption>}}</buzo>''' % (insta_id)

        # replace with markdown
        if md != '':
            strungsoup = strungsoup.replace(check, md)
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
    
    # Headings
    headings = soup.find_all(['h1','h2','h3','h4','h5','h6'])
    if len(headings) > 0:
        for h in headings:
            if h.name in ['h1','h2','h3']:
                level = "\n### "
            elif h.name in ['h4','h5','h6']:
                level = "\n#### "
            h = ' '.join(h.get_text().split())
            if h in value:
                value[value.index(h)] = level + h + "\n"
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
        listparts = l.find_all('li')
        for i in listparts:
            count += 1
            replacement = ' '.join(i.get_text().split())
            if replacement in value:
                value.remove(replacement)
            if i.parent.name == 'ol':
                line = str(count) + '. ' + replacement
            elif i.parent.name == 'ul':
                line = "* " + replacement
            
            if count == (len(l.find_all('li'))):
                line +=  '\n\n'
            else:
                line +=  '\n'
            mdli.append(line.lstrip())
        # find insert index from first <li> element
        tracer = ' '.join(listparts[0].find_previous(['p','h5','h4','h3','h2','h1','span','div']).get_text().split())
        try:
            lindex = value.index(tracer)
            value = value[:lindex+1] + mdli + value[lindex+1:]
        except IndexError:
            pass
    return value

# footnotes - bottom link
# rewrite this to make use of links rather than superscript tags
# because there might be superscripts like †*ˆ or just text
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
        prop = value[findex+i+1].strip()
        # if prop[0] != sups[i].get_text()[0]:
        #     prop = "[^" + sups[i].get_text() + "]:" + sups[i].get_text() + ". " + prop[len(sups[i].get_text())-1:] + '\n'
        # else:
        num = sups[i].get_text()
        if int(num) < 10:
            value[findex+i+1] = "[^" + sups[i].get_text() + "]:" + prop[len(sups[i].get_text())-1:]  + '\n'
        elif int(num) < 99:
            value[findex+i+1] = "[^" + sups[i].get_text() + "]:" + prop[len(sups[i].get_text())-2:]  + '\n'
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

headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0", 'From': 'buzo@buzo.dog'}
# url = 'https://themargins.substack.com/p/3-thoughts-on-cars'
url = 'https://markmanson.net/why-you-should-quit-the-news'
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