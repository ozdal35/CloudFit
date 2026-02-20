"""
Django settings for myproject project.
Azure Compatible & Local Friendly Version.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# .env dosyasını yükle (Lokalde çalışırken şifreleri buradan alır)
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# SECURITY CONFIGURATION (Environment Variables)
# =========================================================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-dev')

# Azure'da False olacak, lokalde True
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Azure'dan gelen host adresini kabul et, yoksa lokale (127.0.0.1) izin ver
ALLOWED_HOSTS = [os.environ.get('DJANGO_ALLOWED_HOSTS', '*')]

# =========================================================
# CSRF TRUSTED ORIGINS (Azure için ŞART!)
# =========================================================
# Eğer Azure domaini Environment Variable olarak gelirse ekle, yoksa senin verdiğin adresi kullan
azure_host = os.environ.get('DJANGO_ALLOWED_HOSTS', 'cloudfit-efe-app2.azurewebsites.net')
CSRF_TRUSTED_ORIGINS = [
    f'https://{azure_host}',
    'https://cloudfit-efe-app-fsevahexgxfgdma9.francecentral-01.azurewebsites.net' # Senin eski yedeğin
]

# =========================================================
# APPLICATION DEFINITION
# =========================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages', # Azure Blob Storage için gerekli!
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # CSS dosyaları için şart!
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# =========================================================
# DATABASE CONFIGURATION (Hard Requirement)
# =========================================================
# Eğer Azure'da DB_HOST şifresini bulursa direkt Azure'a bağlanır.
# Bulamazsa kendi bilgisayarındaki sqlite3 veritabanını kullanır.
if 'DB_HOST' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=f"postgres://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:5432/{os.environ.get('DB_NAME')}",
            conn_max_age=600
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# =========================================================
# PASSWORD VALIDATION
# =========================================================
AUTH_PASSWORD_VALIDATORS = []

# =========================================================
# INTERNATIONALIZATION
# =========================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =========================================================
# STATIC FILES (CSS, JavaScript)
# =========================================================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =========================================================
# MEDIA FILES (Pictures) & AZURE BLOB STORAGE (Soft Requirement)
# =========================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Eğer Azure Connection String bulursa, resimleri buluta kaydeder
if 'AZURE_CONNECTION_STRING' in os.environ:
    DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
    AZURE_CONNECTION_STRING = os.environ.get('AZURE_CONNECTION_STRING')
    AZURE_CONTAINER = 'media'

# =========================================================
# AUTH REDIRECTS
# =========================================================
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'