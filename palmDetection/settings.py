"""
Django settings for palmDetection project.

مهيأ للعمل محليًا وللإنتاج:
- WhiteNoise لخدمة static
- قاعدة بيانات: SQLite محليًا، وPostgreSQL عبر DATABASE_URL على الإنتاج
"""

from pathlib import Path
import os
import dj_database_url

# ================== المسارات الأساسية ==================
BASE_DIR = Path(__file__).resolve().parent.parent

# ================== الأمان / البيئة ==================
# في الإنتاج: عيّني SECRET_KEY من متغير بيئي ولا تتركي قيمة ثابتة داخل الكود
SECRET_KEY = os.getenv("SECRET_KEY", "dev-insecure-change-me")

# محليًا True، وعلى الإنتاج اضبطي DEBUG=False من متغير بيئي
DEBUG = os.getenv("DEBUG", "True").lower() in {"1", "true", "yes", "y"}

# أضيفي نطاق Northflank الفرعي أو الدومين الخاص بك من المتغير البيئي
ALLOWED_HOSTS = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()]

# لحماية CSRF عند وجود دومين/بروكسي أمام التطبيق (أضيفي روابط https كاملة)
# مثال: https://your-subdomain.northflank.app
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]

# ================== التطبيقات ==================
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",   # يُعطّل static الافتراضي لـ runserver ليستعمل WhiteNoise
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "base",
]

# ================== الميدلوير ==================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # مباشرة بعد SecurityMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "palmDetection.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "palmDetection.wsgi.application"

# ================== قواعد البيانات ==================
# محليًا: SQLite (بدون SSL)
# إنتاجًا: PostgreSQL من DATABASE_URL مع SSL
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if DATABASE_URL:
    # إنتاج (Postgres مع SSL)
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,   # SSL للإنتاج فقط
        )
    }
else:
    # تطوير محلي (SQLite) — لا يوجد sslmode هنا
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ================== كلمات المرور ==================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ================== اللغة والمنطقة الزمنية ==================
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Riyadh")  # منطقتك الزمنية
USE_I18N = True
USE_TZ = True

# ================== الملفات الثابتة والوسائط ==================
# Static
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # يجمع إليها collectstatic على الإنتاج
# أثناء التطوير قد تملكين مجلد static محلي
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")] if (BASE_DIR / "static").exists() else []
# WhiteNoise: تخزين مضغوط مع Manifest للهاش
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media (للملفات المرفوعة)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ================== مفاتيح افتراضية ==================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# لو عندك موديل مستخدم مخصص:
AUTH_USER_MODEL = "base.UserAccount"

# بعد تسجيل الخروج
LOGOUT_REDIRECT_URL = "/"

# ================== إعدادات أمان إضافية (إنتاج) ==================
if not DEBUG:
    # إجبار HTTPS إذا كان لديك TLS أمام التطبيق
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "true").lower() in {"1", "true", "yes", "y"}
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HSTS (فعّليه عندما تتأكدي أن الموقع يعمل دائمًا على HTTPS)
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))  # سنة
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
