#!/usr/bin/env python3
from urllib.parse import (
    urlsplit, urlunsplit, urljoin,
    quote, quote_plus,
    parse_qsl, urlencode, urldefrag
)
from html import escape

links = open("links.txt", mode="rt", encoding="utf-8", errors="strict")
links = links.read().split("\n")
used = []
[x for x in links if x not in used and (used.append(x) or True)]
x = ""  # previous value, auto-setting https to where there's no scheme

o2=[]
for i in range(0, len(used)):
    try: comment=used[i].split(" ~ ",1)[1]
    except IndexError: comment=False
    a=used[i].split(" ~ ",1)[0]
    b = list(urlsplit(a))
    if b == ['', '', '', '', '']:  # skip empty item(s)
        continue


    if b[0] == b[1] == "":
        split=b[2].split("/")
#        print("↓EMPTY PROTO & HOST")
#        print("host old",b[1])
        b[1]=split[0]
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
    displayname=a if not comment else comment
    o2+=[f"<li><pre><span><a href=\"{i+1:>1}\">{i+1:>3}| </a></span><a id=\"{i+1:>1}\" href='{url}'>"+escape(displayname)+"</a></pre></li>"]
    x = url

#output before list
o1="""<html><head><title>bookmarklist.py</title>
<link rel="stylesheet" type="text/css" href="style.css" media="screen"/>
</head><body><ul>
"""
#output after list
o3="""
</ul></body></html>"""

o=""
#print(o1)
#for i in o2: print(i)
#print(o3)

f=open("x.html", "w")
f.write(o1)
for i in o2: f.write(i+"\n")
f.write(o3)
