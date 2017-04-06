# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

import os
import djcelery

djcelery.setup_loader()

BASEDIR = os.path.dirname(os.path.abspath(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# ID 1 is reserved for development/testing site
SITE_ID = 1

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASEDIR, 'database.db'),
  }
}

TIME_ZONE = 'Europe/Helsinki'

LANGUAGE_CODE = 'fi-fi'

LANGUAGES = (
  ('fi', 'FI'),
  ('en', 'EN'),
  ('sv', 'SV'),
)

LOCALE_PATHS = (
  os.path.join(BASEDIR, 'locale'),
)

STATICFILES_DIRS = (
  os.path.join(BASEDIR, 'static'),
)

STATIC_ROOT = os.path.join(BASEDIR, '..', 'staticroot')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  'compressor.finders.CompressorFinder',
)

COMPRESS_PARSER = 'compressor.parser.HtmlParser'

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False

COMPRESS_CSS_FILTERS = [
  'compressor.filters.css_default.CssAbsoluteFilter',
  'hutils.compressor_filters.ScssFilter',
]
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASEDIR, '..', 'mediaroot')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/static/admin/'

MIDDLEWARE_CLASSES = (
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'dreamsso.middleware.OrganisationSelectMiddleware',
  'dreamcards.middleware.LanguageSelectMiddleware',
  'django.middleware.locale.LocaleMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATE_LOADERS = (
  'apptemplates.Loader',
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
  'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(BASEDIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
  'dreamcards.context_processors.defaults',
  'django.contrib.auth.context_processors.auth',
  'django.core.context_processors.debug',
  'django.core.context_processors.i18n',
  'django.core.context_processors.media',
  'django.core.context_processors.static',
  'django.core.context_processors.tz',
  'django.contrib.messages.context_processors.messages',

)

INSTALLED_APPS = (
  # admin needs to be first, otherwise circular import with gunicorn
  'django.contrib.admin',

  'longerusername',
  'airo',
  'simplevideos',
  'moodle',
  'wilma',
  'dreamcards',
  'dreamdikaios.dreamdikaiosdreamcards',
  'dreamdikaios.dreamdikaiosusers',
  'dreamsso',
  'dreamuserdb',

  'djcelery',
  'compressor',
  'rest_framework',
  'imagekit',

  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.humanize',
  'django.contrib.sessions',
  'django.contrib.staticfiles',
  'django.contrib.messages',
)

AUTHENTICATION_BACKENDS = (
  'dreamsso.authbackend.local.SingleDatabaseBackend',
  'airo.authbackend.AiroShibbolethBackend',
)

MAX_USERNAME_LENGTH = 2048

SIMPLEVIDEOS_PLAYLIST_CACHE_EXPIRY = 60
SIMPLEVIDEOS_VIDEO_CACHE_EXPIRY = 60
SIMPLEVIDEOS_REQUIRE_LOGIN = True

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

REST_FRAMEWORK = {
  'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAuthenticated',
  )
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

APPEND_SLASH = False

SHIBBOLETH_HEADER_USERNAME = 'HTTP_USERNAME'

AIRO_USERADMIN_PERMISSION_FILTER = (('airo', 'airo', 'supervisor'), ('airo', 'airo', 'user'))

DREAMUSERDB_DOMAIN = 'http://localhost:8000'
DREAMUSERDB_CHECK_USERNAME_FORMAT = False
DREAMSSO_USER_PTR_RELATED_NAME = 'dreamsso_user'

DREAMCARDS_CARD_SERIALIZERS = {
  'edustorecard': 'dreamdikaios.dreamdikaiosdreamcards.serializers.EdustoreCardSerializer',
}

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

