
"""
This settings are for testing Pathagar with the Django development
server.  It will use a SQLite database in the current directory and
Pathagar will be available at http://127.0.0.1:8000 loopback address.

For production, you should use a proper web server to deploy Django,
serve static files, and setup a proper database.

"""


import os


# Books settings:

BOOKS_PER_PAGE = 20 # Number of books shown per page in the OPDS
                    # catalogs and in the HTML pages.

BOOKS_STATICS_VIA_DJANGO = True

# sendfile settings:

SENDFILE_BACKEND = 'sendfile.backends.development'

# Get current directory to get media and templates while developing:
CUR_DIR = u'' + os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(CUR_DIR, 'database.db'),
    }
}

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = os.path.join(CUR_DIR, 'static_media')

MEDIA_URL = '/static_media/'

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = '7ks@b7+gi^c4adff)6ka228#rd4f62v*g_dtmo*@i62k)qn=cs'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'pathagar.urls'

INTERNAL_IPS = ('127.0.0.1',)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'tagging', # TODO old
    'taggit',
    'pathagar.books'
)
