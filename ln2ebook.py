#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import argparse
import shutil

from urls import validate_url
from epub import EpubBook


if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description='Generate ebook files from web sources.')
    parser.add_argument('url', metavar='URL', nargs=1,
                        help='url of novel (only supports lightnovel.cn urls for now), support short-hand such as ln:<id> for lightnovel.cn')
    parser.add_argument('output', metavar='OUTPUT', nargs=1,
                        help='output file name')
    parser.add_argument('--clear-cache', action='store_true')
    parser.add_argument('-f', '--format', 
                        help='output ebook format (EPUB only for now)')
    parser.add_argument('-u', '--user', 
                        help='user account for the resource')
    args = parser.parse_args()

    # Get the approriate handler for the resource url
    handlers, url = validate_url(args.url[0])
    res_handler, login_handler = handlers
    
    # User authentication
    username = args.user
    if username:
        login = login_handler(username)
        login.login()
    
    # Parsing and output
    resource = res_handler(url)
    resource.output_book(EpubBook, args.output[0])

