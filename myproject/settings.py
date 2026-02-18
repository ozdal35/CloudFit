"""
Django settings for myproject project.
Azure Compatible & Local Friendly Version.
"""

import dj_database_url
from pathlib import Path
import os
from dotenv import load_dotenv

# .env dosyasını yükle (Lokalde çalışırken şifreleri buradan alır)
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# SECURITY CONFIGURATION (Environment Variables)
# =========================================================
# Azure'da Environment Variable olarak tanımlayacağız, yoksa .env'den okur
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-for-dev')

# Azure'da False olacak, lokalde True
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Azure domainini buraya ekleyeceğiz. Şimdilik '*' diyerek herkese izin veriyoruz.
ALLOWED_HOSTS = ['*']


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
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <-- EKLENDİ: CSS dosyaları için şart!
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
# DATABASE CONFIGURATION
# =========================================================
# Eğer 'DATABASE_URL' diye bir ayar varsa (Azure), onu kullan.
# Yoksa (Local), bilgisayardaki db.sqlite3 dosyasını kullan.

DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}


# =========================================================
# PASSWORD VALIDATION (Eğitim amaçlı basitleştirildi)
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
# STATIC FILES (CSS, JavaScript, Images)
# Azure için kritik ayarlar burası
# =========================================================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Azure dosyaları burada toplar

# Whitenoise storage (Dosyaların sıkıştırılması ve önbelleğe alınması için)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Files (Yüklenen resimler için)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# =========================================================
# AUTH REDIRECTS
# =========================================================
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'