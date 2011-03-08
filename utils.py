# -*- coding: utf-8 -*-
import collections
from lxml.html.clean import Cleaner
from mako.lookup import TemplateLookup


lookup = TemplateLookup(directories=['./templates'],
                        module_directory='/tmp/mako_modules')
def render(template_path, **context):
    template = lookup.get_template(template_path)
    return template.render(**context)

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
