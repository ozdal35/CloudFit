"""
Django settings for myproject project.
Azure Compatible & Local Friendly Version - FINAL.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# .env dosyasını yükle (Lokalde çalışırken şifreleri buradan alır)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# SECURITY CONFIGURATION
# =========================================================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-dev')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Azure'dan gelen host adreslerini kabul et
ALLOWED_HOSTS = ['*'] # En garantisi budur, hata payını sıfırlar.

# =========================================================
# CSRF TRUSTED ORIGINS (Azure için ŞART!)
# =========================================================
CSRF_TRUSTED_ORIGINS = [
    'https://cloudfit-efe-app2.azurewebsites.net',
    'https://cloudfit-efe-app2-gcczg6daevepevgv.francecentral-01.azurewebsites.net' # Loglardaki uzun adresin
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
    'storages', 
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
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
# DATABASE CONFIGURATION (SSLMODE EKLENDİ!)
# =========================================================
if 'DB_HOST' in os.environ:
    # Azure Flexible Server için sslmode=require zorunludur!
    db_url = f"postgres://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:5432/{os.environ.get('DB_NAME')}?sslmode=require"
    DATABASES = {
        'default': dj_database_url.config(
            default=db_url,
            conn_max_age=600,
            ssl_require=True
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
# STATIC & MEDIA FILES
# =========================================================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

if 'AZURE_CONNECTION_STRING' in os.environ:
    DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
    AZURE_CONNECTION_STRING = os.environ.get('AZURE_CONNECTION_STRING')
    AZURE_CONTAINER = 'media'

# =========================================================
# AUTH REDIRECTS & OTHER SETTINGS
# =========================================================
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'