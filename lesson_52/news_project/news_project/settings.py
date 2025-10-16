"""
Django settings for news_project project.
Optimized for both development and production environments.
"""

from pathlib import Path
from decouple import config

# === BASE DIRECTORY ===
BASE_DIR = Path(__file__).resolve().parent.parent


# === SECURITY SETTINGS ===
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'django-mohirdev-demo.uz',
    'www.django-mohirdev-demo.uz',
]


# === APPLICATIONS ===
INSTALLED_APPS = [
    # Whitenoise — runserverda Django staticni o‘chiradi
    "whitenoise.runserver_nostatic",

    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local apps
    "news_app",
    "widget_tweaks",
    "accounts.apps.AccountsConfig",
]


# === MIDDLEWARE ===
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # Whitenoise staticlarni xizmat qiladi (DEBUG=False bo‘lsa ham)
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# === URL CONFIGURATION ===
ROOT_URLCONF = "news_project.urls"


# === TEMPLATES ===
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                # Custom context processor
                "news_app.context_processor.latest_news",
            ],
        },
    },
]


# === WSGI APPLICATION ===
WSGI_APPLICATION = "news_project.wsgi.application"


# === DATABASE ===
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# === PASSWORD VALIDATION ===
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# === INTERNATIONALIZATION ===
LANGUAGES = (
    ('uz', 'Uzbek'),
    ('en', 'English'),
    ('ru', 'Russian'),
)

LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [BASE_DIR / 'locale']


# === STATIC & MEDIA SETTINGS ===
STATIC_URL = '/static/'

# Local development paytida ishlatiladigan static papka
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Production yoki local bo‘lishiga qarab yo‘lni aniqlaymiz
if not DEBUG:  # Production
    STATIC_ROOT = '/home/djangomo/django-mohirdev-demo.uz/django/staticfiles'
    MEDIA_ROOT = '/home/djangomo/django-mohirdev-demo.uz/django/media'
else:  # Development
    STATIC_ROOT = BASE_DIR / "staticfiles"
    MEDIA_ROOT = BASE_DIR / "media"

# WhiteNoise — static fayllarni siqib, cache bilan tez xizmat qiladi
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'

# === SECURITY (Production uchun) ===
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'


# === LOGIN SETTINGS ===
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'news:home'


# === EMAIL SETTINGS ===
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.example.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your_email@example.com'
# EMAIL_HOST_PASSWORD = 'your_email_password'
# DEFAULT_FROM_EMAIL = 'your_email@example.com'


# === DEFAULT PRIMARY KEY FIELD ===
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
