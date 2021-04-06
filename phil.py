#!/usr/bin/env python3
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import urllib.parse
import collections
import re


def get_content(name):
    url = "https://ru.wikipedia.org/wiki/" + urllib.parse.quote(name)
    try:
        with urlopen(url) as f:
            page = f.read().decode('utf_8')
        return page
    except (URLError, HTTPError):
        return None
    pass


notes_id = ".D0.9F.D1.80.D0.B8.D0.BC.D0.B5.D1.87.D0.B0.D0.BD.D0.B8.D1.8F"
links_id = ".D0.A1.D0.BC._.D1.82.D0.B0.D0.BA.D0.B6.D0.B5"
literature_id = ".D0.9B.D0.B8.D1.82.D0.B5.D1.80.D0.B0.D1.82.D1.83.D1.80.D0.B0"
look_also_id = ".D0.A1.D1.81.D1.8B.D0.BB.D0.BA.D0.B8"


def extract_content(page):
    begin = page.find("mw-parser-output") + len("mw-parser-output") + 1
    if begin == -1:
        return 0, 0
    end = page.find(look_also_id)
    if end == -1:
        end = page.find(notes_id)
        if end == -1:
            end = page.find(literature_id)
            if end == -1:
                end = page.find(links_id)
                if end == -1:
                    end = len(page) - 1
    return begin, end
    pass


def extract_links(page, begin, end):
    f = page[begin:end]
    links = re.findall(r"/wiki/([%\w]*)[\"\']", f)
    ans = set()
    for link in links:
        s = urllib.parse.unquote(link)
        ans.add(s)
    return ans
    pass


def find_chain(start, finish):
    if start.casefold() == finish.casefold():
        return [start]
    visited = set()
    queue = collections.deque([(start, [])])
    visited.add(start)
    while queue:
        vertex, path = queue.popleft()
        visited.add(vertex)
        page = get_content(vertex)
        if page is None:
            continue
        else:
            begin, end = extract_content(page)
            links = extract_links(page, begin, end)
        for neighbour in links:
            if neighbour.casefold() == finish.casefold():
                return path + [vertex, neighbour]
            if neighbour in visited:
                continue
            queue.append((neighbour, path + [vertex]))
            visited.add(neighbour)
    return None


def main():
    pass


if __name__ == '__main__':
    main()
