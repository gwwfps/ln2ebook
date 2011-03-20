#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import argparse
import shutil

from urls import validate_url
from epub import EpubBook


url = 'http://www.lightnovel.cn/viewthread.php?tid=252294'
output = 'test.epub'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate ebook files from web sources.')
    parser.add_argument('url', metavar='URL', nargs=1,
                        help='url of novel (only supports lightnovel.cn urls for now), support short-hand such as ln:<id> for lightnovel.cn')
    parser.add_argument('output', metavar='OUTPUT', nargs=1,
                        help='output file name')
    parser.add_argument('--clear-cache', action='store_true')
    parser.add_argument('-f', '--format', 
                        help='output ebook format (EPUB only for now)')
    args = parser.parse_args()
    
    handler, url = validate_url(args.url[0])
    resource = handler(url)
    resource.output_book(EpubBook, args.output[0])


