#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import argparse

from urls import validate_url
from utils import cj
from epub import EpubBook
from mobi import MobiBook


output_classes = {
    'mobi': MobiBook,
    'epub': EpubBook
}

if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description='Generate ebook files from web sources.')
    parser.add_argument('url', metavar='URL', nargs=1,
                        help='url of novel (only supports lightnovel.cn urls for now), support short-hand such as ln:<id> for lightnovel.cn')
    parser.add_argument('output', metavar='OUTPUT', nargs=1,
                        help='output file name')
    parser.add_argument('--clear-cache', action='store_true')
    parser.add_argument('-u', '--user', 
                        help='user account for the resource')
    parser.add_argument('-k', '--kindlegen',
                        help='path to kindlegen executable (for MOBI only)')
    args = parser.parse_args()

    # Get the approriate handler for the resource url
    handlers, url = validate_url(args.url[0])
    res_handler, login_handler = handlers
    
    # User authentication
    username = args.user
    if username:
        login = login_handler(username)
        logged_in = False
        while not logged_in:
            logged_in = login.login()
    
    # Parsing and output
    resource = res_handler(url)
    out_fn = args.output[0]
    out_cls = output_classes.get(out_fn.split('.')[-1], output_classes['epub'])
    resource.output_book(out_cls, out_fn, args)

    cj.save('.cookies')
