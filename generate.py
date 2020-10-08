#!/usr/bin/env python3
from urllib.parse import (
    urlsplit, urlunsplit,
    quote, quote_plus,
    parse_qsl, urlencode, urljoin, urldefrag
)
links = open("links.txt", mode="rt", encoding="utf-8", errors="strict")
links = links.read().split("\n")
used = []
[x for x in links if x not in used and (used.append(x) or True)]
x = ""  # previous value, auto-setting https to where there's no scheme
for i in range(0, len(used)):
    a = urlsplit(used[i])
    b = list(a)
    if b == ['', '', '', '', '']:  # skip empty item(s)
        continue
    # urlencode the path, keeping slashes intact
    # add more safe chars when needed, use quote_plus to s/ /+/g
    b[2] = quote(a[2], safe="/", encoding="utf-8", errors="strict")
    # empty query values are added on! ?key=val&key -> ?key=val&key=
    query = parse_qsl(a[3], keep_blank_values=True, errors="strict")
    # taking the empty queries and putting them on the end alone,
    # without extra "=" marks
    qn = -1
    empty_q = []
    for q in query:
        qn += 1
        if q[1] == "":
            a = query.pop(qn)[0]
            empty_q += [quote_plus(a)]
    b[3] = urlencode(query)
    for q in empty_q:
        b[3] += "&"+q
    print(b[3])
    try:
        b[4] = quote(a[4])
    except Exception:
        pass
    nr = f"{i+1:>3}|"
    url = urlunsplit(b)
    print(nr, url)
    x = url
