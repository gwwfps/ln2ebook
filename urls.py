# -*- coding: utf-8 -*-
from urlparse import urlparse

from lightnovelcn import LNThread, LNLogin


class UnsupportedURL(Exception): pass

domain_handlers = {
    'www.lightnovel.cn': (LNThread, LNLogin)
}
shortcuts = {
    'ln': lambda pr: 'http://www.lightnovel.cn/thread-{}-1-1.html'.format(pr.netloc)
}

def validate_url(url):
    pr = urlparse(url, 'http')

    if pr.scheme == 'http' and pr.netloc in domain_handlers:
        return domain_handlers[pr.netloc], pr.geturl()
    elif pr.scheme in shortcuts:
        return validate_url(shortcuts[pr.scheme](pr))
    else:
        raise UnsupportedURL
