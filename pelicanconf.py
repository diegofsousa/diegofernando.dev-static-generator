 
#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import datetime

AUTHOR = u'Diego Fernando'
SITENAME = u'Diego Fernando'
SITESUBTITLE = "Entusiasta de tecnologia e programador"
SITEURL = 'https://diegofernando.dev'

PATH = 'content'

DEFAULT_DATE = 'fs'

DEFAULT_DATE_FORMAT = '%d %b %Y'

LOCALE = 'pt_BR.UTF-8'

TIMEZONE = 'America/Fortaleza'

# guess_lang=False: only highlight fenced blocks that declare a language
# (```go, ```python, ...). Guessing was mislabeling untagged Go snippets.
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'guess_lang': False,
        },
        'markdown.extensions.toc': {
            'permalink': '#',
            'permalink_title': 'Link direto para esta seção',
            # The page already has its own h1 (site brand) and h2 (post
            # title); shift markdown's `#`/`##` down so headings stay in
            # sequential order instead of jumping back to h1 mid-document.
            'baselevel': 3,
        },
    },
    'output_format': 'html5',
}

DEFAULT_LANG = u'pt-br'
# og:locale for Open Graph tags — was falling back to the theme's hardcoded
# 'en_US' default on every page, including pt-br ones.
OG_LOCALE = 'pt_BR'

# Fallback social-share image for pages/articles without their own
# og_image (the theme had no images/home-bg.jpg of its own, so this was
# silently 404ing on every page that fell through to it).
HEADER_COVER = 'assets/images/diegocapa.jpg'

# llms.txt — plain-text site summary for LLM agents (not an official spec
# yet, but a growing convention). Rendered from theme-terminal/templates/
# llms.html on every build, one per (sub)site, so it never goes stale.
DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'authors', 'archives', 'llms']
LLMS_SAVE_AS = 'llms.txt'
LLMS_URL = 'llms.txt'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('Facebook', 'http://facebook.com/arulraj.net'),
          ('Twitter', 'http://twitter.com/arulrajnet')
          )

# Pagination
DEFAULT_PAGINATION = 3
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

STATIC_PATHS = ['assets']

EXTRA_PATH_METADATA = {
    'assets/robots.txt': {'path': 'robots.txt'},
    'assets/favicon.ico': {'path': 'favicon.ico'},
    'assets/CNAME': {'path': 'CNAME'}
}

# Post and Pages path
ARTICLE_URL = '{slug}.html'
ARTICLE_SAVE_AS = '{slug}.html'
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'

# Tags and Category path
CATEGORY_URL = 'category/{slug}'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
CATEGORIES_SAVE_AS = 'catgegories.html'
TAG_URL = 'tag/{slug}'
TAG_SAVE_AS = 'tag/{slug}/index.html'
TAGS_SAVE_AS = 'tags.html'

# Author
AUTHOR_URL = 'author/{slug}'
AUTHOR_SAVE_AS = 'author/{slug}/index.html'
AUTHORS_SAVE_AS = 'authors.html'

### Plugins

PLUGIN_PATHS = [
  'pelican-plugins'
]

PLUGINS = [
  'sitemap',
  'neighbors',
  'assets',
  'i18n_subsites',
]

# Sitemap
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

# Comments (giscus — https://giscus.app)
GISCUS_REPO = 'diegofsousa/diegofsousa.github.io'
GISCUS_REPO_ID = 'MDEwOlJlcG9zaXRvcnkxMTAwOTM0NTE='
GISCUS_CATEGORY = 'General'
GISCUS_CATEGORY_ID = 'DIC_kwDOBo_ki84DFguP'


THEME = 'theme-terminal'

### Theme specific settings

CURRENT_YEAR = datetime.date.today().year

AUTHORS_BIO = {
  "diego": {
    "name": "Diego Fernando",
    "cover": "assets/images/diegocapa.jpg",
    "image": "assets/images/eu-df.jpeg",
    "website": "https://diegofernando.dev",
    "linkedin": "diegofsousa",
    "github": "diegofsousa",
    "location": "Brasil",
    "bio": "Engenheiro de software. Entusiasta de sistemas distribuídos, linguagens de programação e música brasileira. Nascido e criado com orgulho no nordeste do Brasil ❤️."
  }
}

### i18n — structure only (see i18n_subsites plugin). Posts stay written
### in whichever single language they were authored in; this only covers
### the site chrome (nav, labels, footer bio) so it doesn't read as a
### mix of English and Portuguese regardless of which subsite renders.

# Every content file must carry a `lang: pt` (or `lang: en`) metadata
# field — i18n_subsites falls back untagged content to DEFAULT_LANG on
# every pass, which would duplicate it across every subsite otherwise.
I18N_UNTRANSLATED_ARTICLES = 'remove'
I18N_UNTRANSLATED_PAGES = 'remove'

I18N_SUBSITES = {
  'en': {
    'SITESUBTITLE': "I'm a technology enthusiast and programmer",
    'LOCALE': 'en_US.UTF-8',
    'DEFAULT_DATE_FORMAT': '%b %d, %Y',
    'OG_LOCALE': 'en_US',
    'MARKDOWN': {
      'extension_configs': {
        'markdown.extensions.toc': {
          'permalink_title': 'Permanent link to this section',
        },
      },
    },
    'AUTHORS_BIO': {
      "diego": {
        **AUTHORS_BIO["diego"],
        "location": "Brazil",
        "bio": "Software Engineer. Enthusiast of distributed systems, programming languages and Brazilian music. Proudly born and raised in northeastern Brazil ❤️.",
      }
    },
  }
}

# UI chrome strings, keyed by DEFAULT_LANG ('pt-br' on the main site,
# 'en' on the i18n_subsites-generated subsite). Templates look these up
# as UI_STRINGS.key[DEFAULT_LANG] — post/page content itself is untouched.
UI_STRINGS = {
  'nav_home':          {'pt-br': 'home',                 'en': 'home'},
  'nav_archives':      {'pt-br': 'arquivo',               'en': 'archives'},
  'nav_tags':          {'pt-br': 'tags',                 'en': 'tags'},
  'nav_search':        {'pt-br': '⌕ buscar',             'en': '⌕ search'},
  'nav_rss':           {'pt-br': '⟁ rss',                'en': '⟁ rss'},
  'latest_posts':      {'pt-br': 'últimos posts',        'en': 'latest posts'},
  'all_posts':         {'pt-br': 'todos os posts',       'en': 'all posts'},
  'categories_label':  {'pt-br': 'categorias',           'en': 'categories'},
  'authors_label':     {'pt-br': 'autores',              'en': 'authors'},
  'posts_tagged':      {'pt-br': 'posts com a tag',      'en': 'posts tagged'},
  'posts_in_category': {'pt-br': 'posts na categoria',   'en': 'posts in category'},
  'posts_by':          {'pt-br': 'posts de',             'en': 'posts by'},
  'pager_page':        {'pt-br': 'página',               'en': 'page'},
  'pager_of':          {'pt-br': 'de',                   'en': 'of'},
  'pager_newer':       {'pt-br': '‹ mais recentes',      'en': '‹ newer'},
  'pager_older':       {'pt-br': 'mais antigos ›',       'en': 'older ›'},
  'breadcrumb_home':   {'pt-br': 'Início',                'en': 'Home'},
  'breadcrumb_posts':  {'pt-br': 'Posts',                'en': 'Posts'},
  'prev':              {'pt-br': '‹ anterior',           'en': '‹ previous'},
  'next':              {'pt-br': 'próximo ›',            'en': 'next ›'},
  'comments':          {'pt-br': 'comentários',          'en': 'comments'},
  'updated_on':        {'pt-br': 'atualizado em',         'en': 'updated on'},
  'search_placeholder':{'pt-br': 'Buscar posts...',      'en': 'Search posts...'},
  'search_close':      {'pt-br': 'Fechar busca',         'en': 'Close search'},
  'search_loading':    {'pt-br': 'carregando índice...', 'en': 'loading index...'},
  'search_unavailable':{'pt-br': 'Busca indisponível no momento.', 'en': 'Search is unavailable right now.'},
  'search_no_results': {'pt-br': 'Nenhum resultado pra', 'en': 'No results for'},
  'copy_label':        {'pt-br': 'copiar',               'en': 'copy'},
  'copied':            {'pt-br': 'copiado!',             'en': 'copied!'},
  'language_switch':   {'pt-br': 'in english',           'en': 'em português'},
  'llms_posts':        {'pt-br': 'Posts',                'en': 'Posts'},
  'llms_pages':        {'pt-br': 'Páginas',              'en': 'Pages'},
}


# Jinja config - Pelican 4
JINJA_ENVIRONMENT = {
  'extensions' :[
    'jinja2.ext.loopcontrols',
    'jinja2.ext.i18n',
    'jinja2.ext.with_',
    'jinja2.ext.do'
  ]
}

JINJA_FILTERS = {'max': max}
JINJA_GLOBALS = {'UI_STRINGS': UI_STRINGS}
# Universal Analytics ("UA-...") was shut down by Google in July 2023 —
# that ID had been collecting nothing since then. Replaced with Cloudflare
# Web Analytics: free, cookieless, no consent banner needed.
CLOUDFLARE_ANALYTICS_TOKEN = "314a3fdb9c9a47e8ba0d1bde9b8636d1"