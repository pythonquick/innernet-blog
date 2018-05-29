#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = 'Guenther'
SITENAME = 'innernet'
SITEURL = 'http://localhost:8000'
SITELOGO = 'https://s.gravatar.com/avatar/fcfe36f97f3eb56b69ecce65d0c895dc?s=80'
ROBOTS = 'index, follow'

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

PATH = 'content'
#THEME = '../pelican-themes/Flex'
#THEME = '../github/Flex'
#THEME = '../github/lannisport'
#THEME = '../github/pelican-mg'
#THEME = '../github/MinimalXY'
#THEME = '../github/pelican-cait'
THEME = '../github/plumage'
#THEME = '../github/pelican-elegant'
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

DISPLAY_CATEGORIES_ON_MENU = False

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('You can squash those links in your config file', '#'),)
LINKS = ()

# Social widget
SOCIAL = (('GitHub', 'https://github.com/pythonquick'),
        ('Twitter', 'https://twitter.com/pythonquick'),)

DEFAULT_PAGINATION = 10

PLUGIN_PATHS = ['../github/pelican-plugins']
PLUGINS = ['gravatar', u'disqus_static', 'sitemap']
DISQUS_SITENAME = u'innernet-1'
DISQUS_SECRET_KEY = os.environ["DISQUS_SECRET_KEY"]
DISQUS_PUBLIC_KEY = u'jHOTvv9aBxf7cXnuBJpPne1SHzMNwMZLFghMrhzBVAx0m3fomH3yulPKaaXJW0k4'
COPYRIGHT = u'© 2018 Guenther Haeussermann'
SITE_THUMBNAIL = 'https://s.gravatar.com/avatar/fcfe36f97f3eb56b69ecce65d0c895dc?s=80'

STATIC_PATHS = ["extras"]

EXTRA_PATH_METADATA = {
    'extras/robots.txt': {'path': 'robots.txt'}
}

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

SITESUBTITLE = "A developer's blog"
