#!/usr/bin/env python3
from urllib.parse import (
    urlsplit, urlunsplit, urljoin,
    quote, quote_plus,
    parse_qsl, urlencode, urldefrag
)
from html import escape
from sys import argv
from os.path import realpath

print(argv)
selfpath=realpath(__file__)
path=selfpath.split("/").pop()
if isinstance(path, str): linksfile="links.txt"
else: linksfile=path+"links.txt" #fallback to links.txt in the repo
outfile="x.html" #fallback
try: linksfile=argv[1] if argv[1]!="all" else linksfile #makefile magic
except IndexError: pass
try: outfile=argv[2]
except IndexError: pass
print("using links from",linksfile)
print("writing output to",outfile)

links = open(linksfile, mode="rt", encoding="utf-8", errors="strict")
links = links.read().split("\n")
used = []
[x for x in links if x not in used and (used.append(x) or True)]
x = ""  # previous value, auto-setting https to where there's no scheme

o2=[]
for i in range(0, len(used)):
    try:
        comment=used[i].split(" ~ ",1)[1]
        a=used[i].split(" ~ ",1)[0]
    except IndexError:
        comment=False
        a=used[i]
    b = list(urlsplit(a))
    if b == ['', '', '', '', '']:  # skip empty item(s)
        continue


    if b[0] == b[1] == "":
        split=b[2].split("/")
#        print("↓EMPTY PROTO & HOST")
#        print("host old",b[1])
#        b[1]=split[0]  #host
        #host must have nothing except alphanum and "-" and "."
        b[1]="".join(list([y for y in split[0] if y.isalnum() or y.replace("-","").isalnum() or y=="."]))
#        print("host new",b[1])
#        print("path old",b[2])
        try:
            b[2]="+"+split[1]+"+"
        except IndexError:
            b[2]=""
        #
#        print("path new",b[2])
#        print("it is",split)


    # urlencode the path, keeping slashes intact
    # add more safe chars when needed, use quote_plus to s/ /+/g
    b[2] = quote(b[2], safe="/", encoding="utf-8", errors="strict")
    # empty query values are added on! ?key=val&key -> ?key=val&key=
    query = parse_qsl(b[3], keep_blank_values=True, errors="strict")
    # taking the empty queries and putting them on the end alone,
    # without extra "=" marks
    qn = -1
    empty_q = []
    for q in query:
        qn += 1
        if q[1] == "":
            #a = query.pop(qn)[0]
            empty_q += [quote_plus(query.pop(qn)[0])]
    b[3] = urlencode(query)
    for q in empty_q:
        b[3] += "&"+q
#    print(b[3])
    try:
        b[4] = quote(b[4])
    except Exception:
        pass


#    print(b)
    url = urlunsplit(b)
    url = urljoin("https://",url,allow_fragments=True)
    #url = url.replace("https:///", "https://", 1)
    displayname=a if comment==False else comment
    
    o2+=[f"<li><pre><span class=\"nr\"><a href=\"#{i+1:>1}\" class=\"nr\" >{i+1:>3}</a></span><a id=\"{i+1:>1}\" href=\"{url}\">"+escape(displayname)+"</a></pre></li>"]
    x = url

#output before list
o1="""<!DOCTYPE html><html><head>
<meta charset="utf-8">
<title>bookmarklist.py</title>
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="stylesheet" type="text/css" href="style.css" media="screen"/>
</head><body>
<img src="favicon.svg"/>
<ul>"""
#output after list
o3="""</ul></body></html>"""

o=""
#print(o1)
#for i in o2: print(i)
#print(o3)

f=open(outfile, "w")
f.write(o1+"\n")
for i in o2: f.write(i+"\n")
f.write(o3+"\n")
