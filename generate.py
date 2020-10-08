#!/usr/bin/env python3
from urllib.parse import (
    urlsplit, urlunsplit, urljoin,
    quote, quote_plus,
    parse_qsl, urlencode, urldefrag
)
links = open("links.txt", mode="rt", encoding="utf-8", errors="strict")
links = links.read().split("\n")
used = []
[x for x in links if x not in used and (used.append(x) or True)]
x = ""  # previous value, auto-setting https to where there's no scheme
for i in range(0, len(used)):
    a = urlsplit(used[i])
    a = list(a)
    b = a
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
    print(b[3])
    try:
        b[4] = quote(b[4])
    except Exception:
        pass


    nr = f"{i+1:>3}|"
    print(b)
    url = urlunsplit(b)
    url = urljoin("https://",url,allow_fragments=True)
    #url = url.replace("https:///", "https://", 1)
    print(nr, url)
    x = url
