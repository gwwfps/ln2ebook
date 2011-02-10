# -*- coding: utf-8 -*-
import httplib2
from pyquery import PyQuery as pq

from utils import flatten


class LNThread(object):
    def __init__(self, url):
        self.url = url
        self.page = self._fetch_page().decode('gbk')
        self.d = pq(self.page)
        self.book_data = self._generate_book_data()

    def output_book(self, filename):
        pass

    def _generate_book_data(self):
        title_parts = self._parse_title()
        translator_uid = self._find_translator_uid()
        chapters = self._find_chapters()

    def _find_chapters(self):
        pass

    def _find_translator_uid(self):
        try:
            # Find UID of thread poster
            return int(self.d('.profile').eq(0).children('dd').eq(0).text())
        except ValueError:
            return None

    def _parse_title(self):
        raw_title = self.d('#threadtitle').text()
        seps = ['[', ']', u'【', u'】', '(', ')']
        title_parts = None
        for sep in seps:
            if title_parts is None:
                title_parts = raw_title.split(sep)
            else:
                title_parts = flatten([part.split(sep) for part in title_parts])
        return filter(bool, [t.strip() for t in title_parts])

    def _fetch_page(self):
        # Assume finished books don't change,
        # so we can just get the content from cache
        cache = httplib2.FileCache('.cache')
        page = cache.get(self.url)
        if page:
            return page
        else:
            h = httplib2.Http('.cache')
            resp, content = h.request(self.url, "GET")
            return content
