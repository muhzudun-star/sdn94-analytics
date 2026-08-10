"""
Django settings for SDN 94 Buton - Sistem Analisis Data Siswa.
"""
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-sdn94-buton-secret-key-ganti-di-produksi-2026'
)

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # third party
    'rest_framework',

    # local apps
    'accounts',
    'akademik',
    'analitik',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.role_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'id-id'
TIME_ZONE = 'Asia/Makassar'
USE_I18N = True
USE_TZ = True

# Static & media files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth redirects (login itu satu pintu, redirect ditentukan di view sesuai role)
LOGIN_URL = 'accounts:login'
LOGOUT_REDIRECT_URL = 'accounts:login'

# ---------------------------------------------------------------------------
# Konfigurasi khusus proyek: Analisis Data Siswa SDN 94 Buton
# ---------------------------------------------------------------------------
# API internal dipakai oleh modul analitik (pandas) untuk mengambil data.
# Semua analisis TIDAK query database secara langsung, melainkan melalui API
# REST yang sudah disediakan oleh app "akademik".
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://127.0.0.1:8000')
INTERNAL_API_KEY = os.environ.get('INTERNAL_API_KEY', 'sdn94-internal-key-2026')

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'akademik.permissions.IsInternalOrAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': None,  # non-paginated -> gampang diolah pandas
}

NAMA_SEKOLAH = "SDN 94 Buton"
