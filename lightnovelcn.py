# -*- coding: utf-8 -*-
from getpass import getpass
from cStringIO import StringIO
from urllib2 import HTTPError
import Image
import ImageOps
import mechanize
from pyquery import PyQuery as pq

from utils import flatten, fetch_url


class LNLogin(object):
    LOGIN_URL = 'http://www.lightnovel.cn/logging.php?action=login'
    SUBMIT_URL = 'http://www.lightnovel.cn/logging.php?action=login&loginsubmit=yes'
    
    def __init__(self, username):
        self.username = username

    def login(self):
        page = fetch_url(self.LOGIN_URL)
        if self.logged_in(page):
            return True
        else:
            forms = mechanize.ParseResponse(mechanize.urlopen(self.LOGIN_URL),
                                            backwards_compat=False)
            form = forms[0]
            form['username'] = self.username
            form['password'] = getpass()
            form.find_control("cookietime").items[0].selected = True

            request = form.click()
            try:
                response = mechanize.urlopen(request)
            except mechanize.HTTPError, response2:
                exit('HTTP error while logging in.')

            content = response.read()
            if self.logged_in(content):
                return True
            else:
                return False
        
    @classmethod
    def logged_in(cls, page):
        return bool(pq(page).find('#loginstatus'))        
        

class LNThread(object):
    def __init__(self, url):
        self.url = url
        self.next_page = 1
        self._turn_page()
        self._generate_book_data()

    def output_book(self, output_cls, filename):
        out = output_cls(self.title, self.chapters, self.images, self.url)
        out.output_to_file(filename)

    def _generate_book_data(self):
        title_parts = self._parse_title()
        self._prompt_title_selection(title_parts)
        self.chapters = []
        self.images = []
        self._translator_uid = self._find_translator_uid()
        self._find_chapters()

    def _prompt_title_selection(self, title_parts):
        for i in range(len(title_parts)):
            print u'{}. {}'.format(i, title_parts[i])
        print 'Choose the correct title:'
        selections = raw_input()
        selections = selections.split(' ')
        self.title = ''.join(title_parts[int(s)] for s in selections)

    def _find_chapters(self):
        for post in self.d('#postlist').children():
            # Assume chapters of a book are contiguous posts made by the thread
            # poster
            try:
                uid = int(pq(pq(post).find('.profile').children('dd')[0]).text())
            except IndexError:
                continue
            if uid == self._translator_uid:
                chapter = self._parse_chapter(post)

                # Find images within the chapter
                for img in chapter.find('img'):
                    self._process_image(img)

                # Remove fluff
                for p in chapter.find('.pstatus'):
                    pq(p).remove()

                self.chapters.append(chapter.html())
            else:
                break
        else:
            self._turn_page()
            self._find_chapters()

    def _turn_page(self):
        url = '{}&page={}'.format(self.url, self.next_page)
        self.page = fetch_url(url).decode('gbk')
        self.d = pq(self.page)
        self.next_page += 1

    def _process_image(self, img):
        pic = pq(img).attr('src')

        # Attachment
        if pic == 'images/common/none.gif':
            pic = 'http://www.lightnovel.cn/{}'.format(pq(img).attr('file'))

        if pic.startswith('http'):
            # Resize/divide image if necessary
            try:
                image_buffer = StringIO(fetch_url(pic))
                image = Image.open(image_buffer)
                # Grayscale size saving too little
                #image = ImageOps.grayscale(image)
                if image.size[0] > image.size[1]:
                    image = image.rotate(90)
                image.thumbnail((600, 800), Image.ANTIALIAS)

                filename = self._add_image(image)
                pq(img).attr('src', filename)
                pq(img).attr('width', str(image.size[0]))
                pq(img).attr('height', str(image.size[1]))
                image_buffer.close()
            except HTTPError:
                print 'Cannot find image: {}'.format(pic)

    def _add_image(self, image):
        filename = 'images/img-{}.jpg'.format(len(self.images))
        out = StringIO()
        image.save(out, 'jpeg')
        self.images.append((filename, out.getvalue()))
        out.close()
        return filename

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
