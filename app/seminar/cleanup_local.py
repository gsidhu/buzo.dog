# Remove \n 
# fix footnotes 
# \\x96 : -
# if title.lower() is in lines[:5], remove that line
# replace spaces in bold and italics
# remove H3 from paragraphs
# add center div 
# fix Books
# fix files without complete names
# turn 'S in title to 's
# -----
# create years page 
# create index page

import re 

import os 
os.chdir("/Users/thatgurjot/Git Repos/seminar/content/posts/")
filenames = os.listdir()
for index in range(len(filenames)):
    # if "Books.md" in filenames[index]:
    #     continue
    # if "7_479" in filenames[index]:
    #     print(filenames[index])
    #     index = index
    #     break

    text = ''
    with open(filenames[index], 'r+') as f:
        text = f.read()

    yaml = text[:text.find("\n---\n")+5]
    body = text[text.find("\n---\n")+5:]
    frontmatter = yaml.split('\n')

    ## add weight
    # wt_num = filenames[index].split('_')[0]
    # weight = 'weight: "' + str(wt_num) + '"'
    # frontmatter = frontmatter[:-2] + [weight] + frontmatter[-2:]
    
    ## fix title
    # title = frontmatter[1].split(': ')
    # title[1] = title[1].replace("'S", "'s")
    # title[1] = title[1].replace("St ", "st ")
    # frontmatter[1] = ': '.join(title)
    # yaml = '\n'.join(frontmatter)

    ## if title exists, remove # line in text 
    # lines = body.split('\n')
    # if len(title[1]) > 0:
    #     for l in range(len(lines)):
    #         try:
    #             if lines[l][:2] == '# ':
    #                 lines.pop(l)
    #         except:
    #             print(filenames[index])
    #             break

    ## fix h3 bold mash (###__This)
    # body = body.replace("#__", '# ')

    ## unnecessary letters
    # body = body.replace('\\n', '')
    # body = body.replace('\\x96', '-')
    
    # lines = body.split('\n')

    ## remove __T and T__\n
    # for i in range(len(lines)):
    #     # T__\n
    #     try:
    #         if "###" in lines[i] and list(lines[i]).count('_') == 2:
    #             lines[i] = lines[i].replace('__', '')
    #         # __and__ > __ and __
    #         elif list(lines[i]).count('_')%4 == 0:
    #             temp = list(lines[i])
    #             under_count = 0
    #             for j in range(len(temp)):
    #                 if temp[j] == '_':
    #                     under_count += 1
    #                     if under_count%4 == 0:
    #                         temp[j] = '_ '
    #                     elif under_count%4 == 1:
    #                         temp[j] = ' _'
    #             lines[i] = ''.join(temp)
    #     except:
    #         print(filenames[index])
    #         break
    

    ## remove duplicate bold lines
    # for i in range(len(lines)):
    #     try:
    #         if "__" in lines[i]:
    #             og_text = lines[i].split('__')[1]
    #             if "__" in lines[i+2]:
    #                 dup_text = lines[i+2].split('__')[1]
    #                 if og_text == dup_text:
    #                     lines.pop(i+2)
    #     except IndexError:
    #         print(filenames[index])
    #         break

    ## remove h3 from paragraphs 
    # for i in range(10):
    #     try:
    #         if "###" in lines[i]:
    #             if len(lines[i].split(' ')) > 15:
    #                 lines[i] = lines[i].replace("###", '')
    #                 break
    #     except IndexError:
    #         print(filenames[index])
    #         break

    ## fix Book headers 
    # for i in range(len(lines)):
    #     if ("###" in lines[i]) or ('__' in lines[i] and 'by' in lines[i]):
    #         temp = lines[i].split('__')
    #         try:
    #             lines[i] = '### ' + temp[1]
    #             lines[i+2] = temp[2]
    #         except IndexError:
    #             print(filenames[index])
    #             break

    ## title replace 
    # frontmatter = yaml.split('\n')
    # fm_title = frontmatter[1].split(' ')

    # for i in range(5):
    #     temp = lines[i].split(' ') # ['#', 'Caste', 'in', 'the', 'periphery']
    #     temp2 = re.sub(r"[^\s\w]", '', lines[i].lower()).split(' ')
    #     toremove = []
    #     # ['title:', '"Caste', 'In', 'The', '\'Periphery\'"']
    #     for word in fm_title:
    #         word = word.lower()
    #         if word in temp:
    #             toremove.append(temp.index(word))
    #         if word in temp2:
    #             toremove.append(temp2.index(word))
    #         word = re.sub(r"[^\s\w]", '', word)
    #         if word in temp:
    #             toremove.append(temp.index(word))
    #         if word in temp2:
    #             toremove.append(temp2.index(word))
    #     temp = [temp[i] for i in range(len(temp)) if i not in toremove]
                
    #     lines[i] = ' '.join(temp)

    ## fix footnotes and references
    # footdex = 0
    # refdex = 0
    # for i in range(len(lines)):
    #     if 'Footnotes' in lines[-1*i]:
    #         footdex = len(lines) - i
    #         lines[footdex] = '__Footnotes__'
    #     if 'References' in lines[-1*i]:
    #         refdex = len(lines) - i
    #         lines[refdex] = '__References__'

    # for i in range(footdex+1,len(lines)):
    #     # if it is a footnote, add proper syntax
    #     if (i < refdex and "[^" in lines[i]):
    #         lines[i] = re.sub(r'(\[\^)+', '', lines[i])
    #         lines[i] = re.sub(r'(\]\:)+', '', lines[i])
    #         temp = lines[i].split(' ')
    #         temp[0] = "[^" + temp[0] + "]:"
    #         lines[i] = ' '.join(temp)
    #     # remove the erroneous syntax from references
    #     elif "[^" in lines[i]:
    #         lines[i] = re.sub(r'(\[\^)+', '', lines[i])
    #         lines[i] = re.sub(r'(\]\:\s)+', '', lines[i])

    # if footdex > 0 and refdex == 0:
    #     for i in range(footdex+1,len(lines)):
    #         if len(lines[i]) > 0:
    #             temp = lines[i].split(' ')
    #             temp[0] = "[^" + temp[0] + "]:"
    #             lines[i] = ' '.join(temp)

    # move references before footnotes 
    # if footdex > 0 and refdex > 0:
    #     lines = lines[:footdex] + lines[refdex:] + lines[footdex:refdex]

    ## download images and change src
    # body = '\n'.join(lines)
    # body = body.replace('\\n', '')

    ## fix bold and italics
    # body = re.sub(r'__ +', '__', body)
    # body = re.sub(r' +__', '__', body)
    # body = re.sub(r'_ +', '_', body)
    # body = re.sub(r' +_', '_', body)
    # body = body.replace('____', '')

    # # fix spaces
    # body = re.sub(r' +', ' ', body)
    # body = re.sub(r'(\n)\n+', '\n\n', body)

    ## remove tab space
    # body = body.replace('\\t', '')

    text = yaml + body 

    with open(filenames[index], 'w+') as f:
        f.write(text)

    # with open('../sas.txt', 'w+') as f:
    #     f.write(text)