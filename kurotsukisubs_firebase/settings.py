"""
Django settings for Kurotsukisubs — Nogizaka46 Fansub Website
Using Firebase Firestore as the database backend.

Copy .env.example to .env and fill in your Firebase credentials.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────────────────────
# BASE PATHS
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

# ─────────────────────────────────────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-i=vwwvw)rjyr@9y%kqfnyo$3t2uxo6a-#frxf#5)z_wx3%jtfq'
)

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ─────────────────────────────────────────────────────────────────────────────
# INSTALLED APPS
# ─────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fansub',
]

# ─────────────────────────────────────────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # serve static files in prod
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kurotsukisubs_firebase.urls'

# ─────────────────────────────────────────────────────────────────────────────
# TEMPLATES
# ─────────────────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Look for templates in the repo-level templates/ directory
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kurotsukisubs_firebase.wsgi.application'

# ─────────────────────────────────────────────────────────────────────────────
# DATABASE
# We use Firebase Firestore — no traditional SQL database needed.
# Django still needs a minimal DB for sessions/auth; use SQLite for that.
# ─────────────────────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# FIREBASE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
# Option A — Service Account JSON file path (recommended for local dev)
FIREBASE_CREDENTIALS_PATH = os.environ.get(
    'FIREBASE_CREDENTIALS_PATH',
    str(BASE_DIR / 'firebase-credentials.json')
)

# Option B — Individual env vars (recommended for production / CI)
FIREBASE_PROJECT_ID      = os.environ.get('FIREBASE_PROJECT_ID', '')
FIREBASE_PRIVATE_KEY_ID  = os.environ.get('FIREBASE_PRIVATE_KEY_ID', '')
FIREBASE_PRIVATE_KEY     = os.environ.get('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n')
FIREBASE_CLIENT_EMAIL    = os.environ.get('FIREBASE_CLIENT_EMAIL', '')
FIREBASE_CLIENT_ID       = os.environ.get('FIREBASE_CLIENT_ID', '')
FIREBASE_CLIENT_CERT_URL = os.environ.get('FIREBASE_CLIENT_CERT_URL', '')

# ─────────────────────────────────────────────────────────────────────────────
# FIREBASE STORAGE (for media uploads)
# ─────────────────────────────────────────────────────────────────────────────
FIREBASE_STORAGE_BUCKET = os.environ.get('FIREBASE_STORAGE_BUCKET', '')

# ─────────────────────────────────────────────────────────────────────────────
# FIRESTORE COLLECTION NAMES
# ─────────────────────────────────────────────────────────────────────────────
FIRESTORE_COLLECTION_POSTS   = 'posts'
FIRESTORE_COLLECTION_MEMBERS = 'members'
FIRESTORE_COLLECTION_TAGS    = 'tags'

# ─────────────────────────────────────────────────────────────────────────────
# PASSWORD VALIDATION
# ─────────────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─────────────────────────────────────────────────────────────────────────────
# INTERNATIONALISATION
# ─────────────────────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True

# ─────────────────────────────────────────────────────────────────────────────
# STATIC & MEDIA FILES
# ─────────────────────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Repo-level static/ directory
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Local media (fallback when Firebase Storage is not configured)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─────────────────────────────────────────────────────────────────────────────
# DEFAULT PRIMARY KEY
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─────────────────────────────────────────────────────────────────────────────
# PAGINATION
# ─────────────────────────────────────────────────────────────────────────────
POSTS_PER_PAGE        = int(os.environ.get('POSTS_PER_PAGE', 5))
MEMBER_POSTS_PER_PAGE = int(os.environ.get('MEMBER_POSTS_PER_PAGE', 12))
RECENT_POSTS_COUNT    = int(os.environ.get('RECENT_POSTS_COUNT', 5))
