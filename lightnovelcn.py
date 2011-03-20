# -*- coding: utf-8 -*-
import httplib2
from pyquery import PyQuery as pq

from utils import flatten, fetch_url


class LNThread(object):
    def __init__(self, url):
        self.url = url
        self.page = self._fetch_page().decode('gbk')
        self.d = pq(self.page)
        self._generate_book_data()

    def output_book(self, output_cls, filename):
        out = output_cls(self.title, self.chapters, self.images, self.url)
        out.output_to_file(filename)

    def _generate_book_data(self):
        title_parts = self._parse_title()
        self._prompt_title_selection(title_parts)
        self._find_chapters()

    def _prompt_title_selection(self, title_parts):
        for i in range(len(title_parts)):
            print u'{}. {}'.format(i, title_parts[i])
        print 'Choose the correct title:'
        selections = raw_input()
        selections = selections.split(' ')
        self.title = ''.join(title_parts[int(s)] for s in selections)

    def _find_chapters(self):
        translator_uid = self._find_translator_uid()
        self.chapters = []
        self.images = []
        for post in self.d('#postlist').children():
            # Assume chapters of a book are contiguous posts made by the thread
            # poster
            try:
                uid = int(pq(pq(post).find('.profile').children('dd')[0]).text())
            except IndexError:
                continue
            if uid == translator_uid:
                chapter = self._parse_chapter(post)

                # Find images within the chapter
                for img in chapter.find('img'):
                    pic = pq(img).attr('src')
                    if pic.startswith('http'):
                        ext = pic.split('.')[-1]
                        pq(img).attr('src',
                                     'images/img-{}.{}'.format(len(self.images),
                                                               ext))
                        self.images.append(pic)

                self.chapters.append(chapter.html())
            else:
                break

    def _parse_chapter(self, post):
        content = pq(post).find('.t_msgfontfix')[0]
        return pq(content)

    def _find_translator_uid(self):
        try:
            # Find UID of thread poster
            return int(pq(self.d('.profile').eq(0).children('dd')[0]).text())
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
            return fetch_url(self.url)
