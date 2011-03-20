# -*- coding: utf-8 -*-
import collections
import httplib2
from lxml.html.clean import Cleaner
from mako.lookup import TemplateLookup


lookup = TemplateLookup(directories=['./templates'],
                        module_directory='/tmp/mako_modules')
def render(template_path, **context):
    template = lookup.get_template(template_path)
    return template.render_unicode(**context).encode('utf-8', 'replace')

# From answer at http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python/2158532#2158532
def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

cleaner = Cleaner()
def clean_html(html):
    return cleaner.clean_html(html)

def fetch_url(url):
    h = httplib2.Http('.cache')
    resp, content = h.request(url, "GET")
    return content
