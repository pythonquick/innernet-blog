#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Guenther'
SITENAME = 'innernet'
SITEURL = 'http://localhost:8000'
SITELOGO = 'https://s.gravatar.com/avatar/fcfe36f97f3eb56b69ecce65d0c895dc?s=80'

PATH = 'content'
THEME = '../pelican-themes/Flex'
MENUITEMS = (('Categories', '/categories.html'),
             ('Tags', '/tags.html'),
             ('Archives', '/archives.html'),)
MAIN_MENU = True
TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('You can squash those links in your config file', '#'),)
LINKS = ()

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

STATIC_PATHS = ["extras"]

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
