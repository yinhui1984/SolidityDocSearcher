#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from importlib.resources import path
import os

from bs4 import BeautifulSoup

# please change to your chrome path
chrome = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'


def get_doc_outline(doc_path, cache_path):
    outlines = []
    if not os.path.exists(cache_path):
        doc_path = os.path.join(os.path.dirname(__file__), doc_path)
        with open(doc_path, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            for heading in soup.find_all(attrs={"class": "headerlink"}):
                # print(heading)
                if heading['href'] not in outlines:
                    outlines.append(heading['href'])
                # 多次出现， 可能比较重要~~ 放前面
                else:
                    outlines.remove(heading['href'])
                    outlines.insert(0, heading['href'])
        # save outlines to file
        with open(cache_path, 'w') as f:
            for outline in outlines:
                f.write(outline + '\n')
    else:
        with open(cache_path, 'r') as f:
            for line in f:
                outlines.append(line.strip())

    return outlines


def search_doc(keyword):
    current_dir = os.path.dirname(__file__)
    indexHtml = os.path.join(current_dir, 'solidity-develop/index.html')
    indexHtml_cn = os.path.join(current_dir, 'solidity-docs-chinese-v0.8.17/index.html')
    outlines_txt = os.path.join(current_dir, 'outlines.txt')
    outlines_cn_txt = os.path.join(current_dir, 'outlines-cn.txt')
    outlines = get_doc_outline(indexHtml, outlines_txt)
    outlines_cn = get_doc_outline(indexHtml_cn, outlines_cn_txt)
    matched = []
    for index, outline in enumerate(outlines):
        if keyword in outline:
            matched.append(outline)

    for href in matched:
        print(str(matched.index(href)).ljust(2), "\t",  href.strip('#').replace('-', ' '))
    index = input("\033[1;32;40mSelect:\033[0m")
    selected = matched[int(index)]
    url = 'file://' + indexHtml + selected
    if selected in outlines_cn:
        url = 'file://' + indexHtml_cn + selected
    cmd = chrome + " " + url
    # print(cmd)
    os.system(cmd)


def main():
    import sys
    if len(sys.argv) > 1:
        search_doc(sys.argv[1])
    else:
        print("Usage: python soldocsearcher keyword")


if __name__ == '__main__':
    main()
