from pprint import pprint as pp

import requests
from bs4 import BeautifulSoup

# create a function to identify main content tags
# and one to decompose tags like -
#   'share', 'related', 'aside', 'nav'
# reverse engineer firefox/readability
# replace <br> with \n and <font> with span

# medium does not load images on first paint
# sometimes the content might be inside divs directly

# sometimes there can be a stray article tag inside an aside like on politico.com
# wrapper function

super_chars = []

def scrape(html, parser, url, title=''):
    soup = BeautifulSoup(html, parser)
    # kill nav
    # soup.find('nav').decompose()

    if True:
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
        elif 'stratechery.com' in url:
            soup = soup.find('article')

        try:
            soup.decompose('aside')
        except:
            pass

        if soup.find('article') != None:
            soup = soup.find('article')
            print('article found')
        if soup.find('main') != None:
            soup = soup.find('main')
        if soup.find('div', class_='content') != None:
            soup = soup.find('div', class_='content')

    soup = images(soup, url)
    soup = tabulate(soup)
    soup = shortcodes(soup)
    soup = strikeembold(soup)
    soup = lists(soup, url)
    soup = links(soup, url)
    soup = headings(soup, url)
    # soup = bquotes(soup)
    soup = superscripts(soup)

    p = soup.find_all(['p','buzo','table'])
    # add markmanson footnotes
    if 'markmanson' in url:
        p.extend(fn)

    text = ''
    value = []
    temp = {'raw':'', 'text':''}
    for tag in p:
        temp['raw'] = str(tag)
        temp['text'] = ' '.join(tag.get_text().split()).strip()
        temp['text'] = temp['text'].replace('&*^', '\n')

        # check if the contents already exist in the last 10 values
        # 10 is to increase efficiency
        # TODO: this could be smaller part of a previous value, so check inside too
        if temp['raw'] in value[-10:] or temp['text'] in value[-10:]:
            continue

        if tag.name == 'table':
            text += '\n' + temp['raw'] + '\n'
            value.append(temp['raw'])
        else:
            text += '\n' + temp['text'] + '\n'
            value.append(temp['text'])

    text = footnotes(text)

    # Cleaning up
    for trash in ['donating = loving', 'Share\nFacebook', 'Like this:\nLike']:
        if trash in text:
            text = text[:text.find(trash)]

    # for seminar 
    if 'india-seminar' in url:
        text.replace('\r\n', '\n')
        lines = text.split('\n')
        # title should be heading 1
        try:
            lines[1] = "# " + lines[1].split('__')[1]
            # author should be heading 3
            lines[3] = "### " + lines[3]
        except:
            lines = ["# " + title] + lines
        text = '\n'.join(lines)

    return text

# fix relative paths for links
def rel_link(link, url):
    trailing_slash = ''
    if link[-1] == '/':
        trailing_slash = '/'
    url_comps = urlmanipulation(url)

    if link[:4] == 'http':
        return link
    if link[0] not in ['/', '.', 'h']:
        link = url_comps['protocol'] + url_comps['tld'] + '/' + '/'.join(url_comps['path_comps'][:-1]) + '/' + link
        return link
    if link[0] == '/':
        prefix = url_comps['protocol'] + url_comps['tld']
        link = prefix + link
        return link
    if link[:2] == './':
        prefix = url
        if prefix[-1] == '/':
            link = prefix + link[2:]
        else:
            link = prefix + link[1:]
        return link
    if '../' in link:
        sploot = link.split('../')
        # replace '' in sploot with path components
        levels = url_comps['path_comps'][:-1]
        for i in range(len(sploot)):
            if sploot[i] == '':
                try:
                    levels.pop(-1)
                except IndexError:
                    pass
        sploot = [i for i in sploot if i != '']
        link = '/' + '/'.join(levels) + '/'
        if link == '//':
            link = '/'
        link += '/'.join(sploot)
        prefix = url_comps['protocol'] + url_comps['tld']
        link = prefix + link + trailing_slash
        return link

# url manipulation
def urlmanipulation(url):
    protocol = url[:url.find('//')+2]
    url = url.replace(protocol,'')
    tld = url[:url.find('/')]
    if '?' in url:
        query = url[url.find('?')+1:]
        url = url.replace(query, '')
    else:
        query = ''
    path = url.replace(tld, '')
    path_components = path.split('/')[1:]
    if '' in path_components:
        path_components.remove('')
    query_parameters = query.split('&')
    
    components = {'protocol': protocol, 'tld': tld, 'query_string': query, 'query_params': query_parameters, 'path_string': path, 'path_comps': path_components}
    return components

# images
def images(soup, url):
    all_images = soup.find_all('img')
    for im in all_images:
        # for seminar
        if 'semarrow%20left' in im['src'] or 'semarrow%20up' in im['src']:
        # if 'alt' in im.attrs and im['alt'] in ["top", "back to issue"]:
            continue
        vals = {'src': '', 'title': '', 'alt': '', 'caption':''}
        if 'data:' in im['src']:
            continue
        if im.next.name == 'figcaption':
            try:
                im.next.find('br').replace_with('\n')
            except AttributeError:
                pass
            vals['caption'] = im.next.text
        
        # fix url
        vals['src'] = rel_link(im['src'], url)
        
        if 'title' in im.attrs.keys():
            vals['title'] = im['title']
        if 'alt' in im.attrs.keys():
            vals['alt'] = im['alt']
        # add p tags so it gets picked up by buzo
        mdimg = '''<buzo class='buzo'>{{< img class="center" data-src="%s" title="%s" alt="%s" caption="%s">}}</buzo>''' % (vals['src'], vals['title'], vals['alt'], vals['caption'])

        # replace original tag
        img_tag = BeautifulSoup(mdimg, 'html5lib')
        img_tag = img_tag.find('buzo')
        im.replace_with(img_tag)
    return soup

# strikethrough, italics and bold
def strikeembold(soup):
    for st in soup.find_all(['em','strike','b','strong']):
        # don't run if it's just one character
        if len(st.get_text().strip()) < 2:
            continue
        
        # turn p and font tags into plain text
        for el in st.find_all(['p', 'font']):
            if len(el.get_text().strip()) > 0:
                el.replace_with(el.get_text().strip())

        # italics
        if st.name == 'em':
            replacement_text = str(st).replace('<em>','_')
            replacement_text = replacement_text.replace('</em>','_')
            replacement_text = ' '.join(replacement_text.split())
            replacement_text = replacement_text.replace(' _', '_')
            replacement_text = replacement_text.replace('_ ', '_')
        # strike
        if st.name == 'strike':
            replacement_text = str(st).replace('<strike>','~~')
            replacement_text = replacement_text.replace('</strike>','~~')
            replacement_text = ' '.join(replacement_text.split())
            replacement_text = replacement_text.replace(' ~~', '~~')
            replacement_text = replacement_text.replace('~~ ', '~~')
        # bold
        if st.name in ['b','strong']:
            replacement_text = str(st).replace(('<'+st.name+'>'),'__')
            replacement_text = replacement_text.replace(('</'+st.name+'>'),'__')
            replacement_text = ' '.join(replacement_text.split())
            replacement_text = replacement_text.replace(' __', '__')
            replacement_text = replacement_text.replace('__ ', '__')
        
        # replace tag with buzo markdown
        replacement_text = "<buzo class='buzo'>" + replacement_text + "</buzo>"
        tag = BeautifulSoup(replacement_text, 'html5lib')
        tag = tag.find('buzo')
        st.replace_with(tag)
    return soup

# blockquotes
def bquotes(soup):
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

# youtube, vimeo, instagram, twitter
def shortcodes(soup):
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

        # replace original tag with buzo markdown
        if md != '':
            tag = BeautifulSoup(md, 'html5lib')
            tag = tag.find('buzo')
            link.replace_with(tag)
    return soup

# links
def links(soup, url):
    all_links = soup.find_all('a')

    for link in all_links:
        if 'href' in link.attrs:
            # for seminar
            if 'india-seminar' in url:
                if '../' in link['href'] or '#top' in link['href']:
                    continue

            # normal run
            lmd = "<buzo class='buzo'>" + "[" + link.get_text() + "](" + rel_link(link['href'], url) + ")" + "</buzo>"
            lmd = BeautifulSoup(lmd, 'html5lib')
            lmd = lmd.find('buzo')
            link.replace_with(lmd)

    return soup

# headings
def headings(soup, url):
    if 'india-seminar' in url:
        return soup
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
            mdh = level + ' '.join(h.get_text().split()) + '\n'
            
            # replace tag with buzo markdown
            mdh = "<buzo class='buzo'>" + mdh + "</buzo>"
            tag = BeautifulSoup(mdh, 'html5lib')
            tag = tag.find('buzo')
            h.replace_with(tag)
    return soup

# lists
def lists(soup, url):
    ols = soup.find_all(['ol','ul'])
    if len(ols) == 0:
        return soup
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
            if i.parent.name == 'ol':
                line = str(count) + '. ' + replacement
            elif i.parent.name == 'ul':
                line = "* " + replacement

            if count == (len(l.find_all('li'))):
                line +=  '\n\n'
            else:
                line +=  '\n'
            mdli.append(line.lstrip())
        
        # replace tag with buzo markdown
        mdli = "<buzo class='buzo'>" + '\n'.join(mdli) + "</buzo>"
        tag = BeautifulSoup(mdli, 'html5lib')
        tag = tag.find('buzo')
        l.replace_with(tag)

    return soup

# footnotes - bottom link
# rewrite this to make use of links rather than superscript tags
# because there might be superscripts like †*ˆ or just text
# and sometimes footnotes might not have a header but they might still have footnotes in class or id 
def footnotes(text):
    if 'Footnotes' not in text:
        return text
    first_index = text.index('Footnotes')
    if text[first_index-2:first_index] == '__':
        first_index = first_index - 2
    slices = text[first_index:].split('\n')
    ref_slices = []
    for s in range(len(slices)):
        if 'References' in slices[s]:
            ref_slices = slices[s:]
            slices = slices[:s]
            break

    for i in super_chars:
        for j in range(len(slices)):
            if i in slices[j][:5]:
                # clean up the dot after 1. 2. 3. ...
                if slices[j][1] == '.':
                    slices[j] = slices[j][0] + slices[j][2:]
                # clean up the dot after 10. 11. 12. ...
                if slices[j][2] == '.':
                    slices[j] = slices[j][:2] + slices[j][3:]
                # clean up 
                if '↵' in slices[j]:
                    slices[j] = slices[j].replace('↵', '')
                # add footnote syntax
                where = slices[j][:5].index(i)
                slices[j] = slices[j][:where] + "[^" + i + "]: " + slices[j][where+len(i):] # len(i) ensures all is covered
                # break so that 1 doesn't mess with 10, 11...
                break
    if ref_slices != []:
        slices = ref_slices + slices
    slice_para = '\n'.join(slices)
    text = text[:first_index] + slice_para
    return text

# footnotes - superscript
def superscripts(soup):
    sups = soup.find_all('sup') # footnotes are all superscript
    for sup in sups:
        super_chars.append(sup.get_text().strip())
        md = "[^" + sup.get_text().strip() + "]"
        sup.replace_with(md)
    return soup

# convert table to markdown
def tabulate(soup):
    tables = soup.find_all('table')
    if len(tables) == 0:
        return soup

    for tb in tables:
        # if there's a buzo tag with an image in the table
        # replace table with buzo tag's contents 
        if len(tb.find_all('buzo')) > 0:
            if "img class" in str(tb.find('buzo')):
                tb.replace_with(tb.find('buzo'))
            continue

        # if there's only one td in the table
        # it's probably being used to center text
        if len(tb.find_all('td')) == 1:
            tb.replace_with(tb.find('td').get_text())
            continue
        # set the strings to hold the data
        markdown_string = ''
        table_header = '|'
        table_header_footer = '|'
        table_rows = ''
        table_header_found = False
        table_header_cell_count = 0
        prev_row_cell_count = 0 # To allow only same number of cells per row
        break_outer_loop = 0

        # if there is a thead we append
        thead = tb.find('thead')
        if thead is not None:
            for td in thead.find_all('td'):
                table_header_cell_count += 1
                table_header_found = True
                table_header += td.get_text().strip() + '|'
                table_header_footer += '--- |'

        # loop all the rows
        for tr in tb.find_all('tr'):
            # get the header if it was not present as thead
            if not table_header_found:
                for th in tr.find_all('th'):
                    table_header_cell_count += 1
                    table_header += th.get_text().strip() + '|'
                    table_header_footer += '--- |'
                    table_header_found = True
            
            # get the cells if they are not in thead
            # thead check 1 - if parent is <thead>, skip iteration
            if tr.find_previous().name == 'thead':
                continue

            table_row = ''
            curr_row_cell_count = 0

            # some tables might have th tags instead of td tags
            # in non-header rows
            tag = 'td'
            if len(tr.find_all('td')) == 0:
                tag = 'th'
            for td in tr.find_all(tag):
                curr_row_cell_count += 1
                table_row += td.get_text().strip() + '|'
            
            # thead check 2 - if markdown row is same as header row from before, skip
            if table_row == table_header:
                continue
            
            # Check that the number of cells match in all the rows
            if prev_row_cell_count != 0 and curr_row_cell_count != prev_row_cell_count:
                # check that it's breaking because of colspan
                if 'colspan' in str(tb):
                    # Show error and break for loop
                    error = "ERROR: Your HTML table rows don't have the same number of cells. Colspan not supported."
                    print(error)
                    # use raw html table in this case (cleaned up)
                    tb.replace_with(clean_table(tb))
                    break_outer_loop = 1
                    break
            
            # only add row if it has data
            if curr_row_cell_count:
                table_rows += '|' + table_row + '\n'
                prev_row_cell_count = curr_row_cell_count
        
        # skip tb loop if using raw html for this table
        if break_outer_loop:
            continue

        # Only do the rest of the processing if 
        # there hasn't been an error processing the rows
        if markdown_string == '':
            # if table header exists
            if table_header_found:
                # Check if the number of cells in header is the same as in rows
                if table_header_cell_count != prev_row_cell_count:
                    error = "ERROR: The number of cells in your header doesn't match the number of cells in your rows."
                    print(error)
                    tb.replace_with(clean_table(tb))
                    continue
            # If table header is missing...
            else:
                # 1. make row 1 header if row 1 is text and next 2 rows are numeric
                rows = table_rows.split('\n')
                if not rows[0].split('|')[1].strip().isnumeric():
                    # checking second element because 0 is first pipe |
                    if rows[1].split('|')[1].strip().isnumeric() and rows[2].split('|')[1].strip().isnumeric():
                        table_header = rows[0]
                        rows.pop(0)
                        table_rows = '\n'.join(rows)
                # OR
                # 2. add an empty header for compatibility with MD processors
                else:
                    table_header = "|" + prev_row_cell_count * '|'
                
                # add header_footer in either case
                table_header_footer = "|" + prev_row_cell_count * '--- |'
            
            # Append header at the beginning
            markdown_string += table_header + '\n'
            markdown_string += table_header_footer + '\n'
            
            # add all the rows
            markdown_string += table_rows

        # hacking newline characters for buzo
        markdown_string = markdown_string.replace('\n', '&*^')

        # new table
        if markdown_string != '':
            markdown_string = '<buzo class="buzo">' + markdown_string + "</buzo>"
            table_tag = BeautifulSoup(markdown_string, 'html5lib')
            table_tag = table_tag.find('buzo')
        
        # replace raw code
        tb.replace_with(table_tag)
    return soup

# cleanup html of table
def clean_table(table):
    for td in table.find_all(['td', 'th']):
        # replace <td> with the text it contains
        td.string = td.get_text()
    
    # remove all style except width and colspan
    for el in table.find_all(['td','th','tbody','thead']):
        td_keys = list(el.attrs.keys())
        for key in td_keys:
            if key not in ["colspan", "width"]:
                el.attrs.pop(key, None)

    # remove all style from table
    table.attrs = {}
    return table

# headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0", 'From': 'buzo@buzo.dog'}
# url = 'http://www.india-seminar.com/2001/508/508%20surinder%20s.%20jodhka.htm'
# r = requests.get(url, headers=headers)
# t = scrape(r.content,'html5lib',url)
# with open('/Users/thatgurjot/Git Repos/seminar/content/sas.txt','w+') as f:
#     f.write(str(t))

# q = strike(t,s)
# with open('./sas.txt','w+') as f:
#     f.write(q)

# url = 'https://themargins.substack.com/p/3-thoughts-on-cars'
# url = 'https://markmanson.net/why-you-should-quit-the-news'
# url = 'https://landing.google.com/sre/sre-book/chapters/monitoring-distributed-systems/'
# url = 'https://medium.com/mozilla-tech/revealing-arch-at-universe-29f4d00c9e58'
# url = 'https://dilemaveche.ro/sectiune/tema-saptamanii/articol/nu-exista-calatorii-decit-cu-trenul-interviu-cu-scriitoarea-nora-iuga'
# url = 'https://www.politico.com/news/2019/12/30/mark-meadows-retirement-elect-wife-friend-090838'
# url = 'http://www.netbits.us/docs/stunnel_rsync.html'
# url = 'http://www.india-seminar.com/2000/494/494%20vincent%20kumaradoss.htm'
# url = 'http://www.india-seminar.com/2018/706/706_yamini_aiyar.htm'
# url = 'http://www.india-seminar.com/1999/479/479%20bose.htm'
# url = 'http://www.india-seminar.com/2018/706/706_rukmini_banerji.htm'
# url = 'http://www.india-seminar.com/2006/564/564_rajeswari_s_raina.htm'
# url = 'http://www.india-seminar.com/2014/654/654_saumen_chattopadhyay.htm'
# url = 'http://www.india-seminar.com/2014/659/659_ranjit_hoskote.htm'
# url = "http://www.india-seminar.com/2014/663/663_nazima_parveen.htm"
# url = 'http://www.india-seminar.com/2015/673/673_vasudha_pande.htm'
# url = 'http://www.india-seminar.com/2016/681/681_debjeet_sarangi_et_al.htm'
# url = 'http://www.india-seminar.com/2018/707/707_pratishtha_pandya.htm'