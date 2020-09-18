# Remove \n 
# fix footnotes 
# \\x96 : -
# if title.lower() is in lines[:5], remove that line
# replace spaces in bold and italics
# -----
# add center div 
# fix Books
# fix files without complete names
# create years page 
# create issues page - add cover image and credits 
# order issues correctly
# remove H3 from paragraphs

import re 

import os 
os.chdir("/Users/thatgurjot/Git Repos/seminar/content/posts/")
filenames = os.listdir()
for index in range(len(filenames)):
    # if "3498_712" in filenames[index]:
    #     print(filenames[index])
    #     index = index
    #     break

    text = ''
    with open(filenames[index], 'r+') as f:
        text = f.read()

    yaml = text[:text.find("\n---\n")+5]
    body = text[text.find("\n---\n")+5:]

    ## unnecessary letters
    # body = body.replace('\\n', '')
    # body = body.replace('\\x96', '-')

    # lines = body.split('\n')

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

    # body = '\n'.join(lines)
    # body = body.replace('\\n', '')

    ## fix bold and italics
    body = re.sub(r'__ +', '__', body)
    body = re.sub(r' +__', '__', body)
    body = re.sub(r'_ +', '_', body)
    body = re.sub(r' +_', '_', body)
    body = body.replace('____', '')

    # # fix spaces
    # body = re.sub(r' +', ' ', body)
    # body = re.sub(r'(\n)\n+', '\n\n', body)

    text = yaml + body 

    with open(filenames[index], 'w+') as f:
        f.write(text)

    # with open('../sas.txt', 'w+') as f:
    #     f.write(text)