import os
from pathlib import Path
from decouple import config
from datetime import timedelta
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-hfxxqcf6&v1dufa(x8cdiuwy3hdv!q2=_qc^(@g!^-b^*tf+g5'
DEBUG = True


PAYPAL_MODE = 'sandbox'  # or 'live' for production
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_SECRET = os.getenv('PAYPAL_SECRET')
PAYPAL_MERCHANT_ID = os.getenv('PAYPAL_MERCHANT_ID')
ALLOWED_HOSTS = [
    "143.198.102.57",
    "143.198.102.57:3000",
    "localhost",
    "127.0.0.1",
    "192.168.100.109",
    "192.168.1.159",
    "192.168.1.154",
    "34.204.95.153",
    "192.168.100.13",
    "198.244.141.33",
    "18.210.33.57",
    "54.160.83.123",
    "patchceb1.ceburu.com",
    "patchmanager.ceburu.com",
]
CORS_ALLOWED_ORIGINS = [
    "http://143.198.102.57",
    "http://143.198.102.57:3000",
    "http://192.168.1.78:3000",
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://34.204.95.153",
    "http://18.210.33.57",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://192.168.100.13",
    "http://198.244.141.33",
    "http://34.204.95.153:3000",
    "http://18.210.33.57:3000",
    "http://192.168.1.159:3000",
    "http://192.168.1.159:3000",
    "http://192.168.1.154:3000",
    "http://54.160.83.123:3000",
    "http://patchceb1.ceburu.com",
    "https://patchmanager.ceburu.com",
    "https://patchceb1.ceburu.com"
]
CORS_ALLOW_CREDENTIALS = True  # Allows sending authentication credentials (cookies, JWT)
CSRF_COOKIE_HTTPONLY = False  # Allow frontend to access CSRF token if needed
CSRF_COOKIE_SECURE = False  # Set to True in production if using HTTPS
CSRF_USE_SESSIONS = True  # Store CSRF token in session
CSRF_TRUSTED_ORIGINS = [
    "http://143.198.102.57",
    "http://143.198.102.57:3000",
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://34.204.95.153",
    "http://18.210.33.57",
    "http://54.160.83.123",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://192.168.1.159:3000",
    "http://192.168.1.159:3001",
    "http://192.168.1.154:3000",
    "http://192.168.1.154:3001",
    "http://localhost:3002",
    "http://192.168.100.13",
    "http://198.244.141.33",
    "https://patchmanager.ceburu.com",
    "http://patchceb1.ceburu.com",
    "https://patchceb1.ceburu.com"
]

CORS_ALLOW_CREDENTIALS = True

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "accounts",
    "corsheaders",
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'rest_framework_simplejwt.token_blacklist',
    'engageiq_app',
    'blog_app',
    'content_manage_app',
    'faqs',
    'ckeditor',
    'ckeditor_uploader',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates"],
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

# WSGI Application
WSGI_APPLICATION = 'django_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Authentication
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Email configuration
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=587)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False) 
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="webmaster@localhost")

# Static files
STATIC_URL = 'static/'
ROOT_URLCONF = 'django_project.urls'

CSRF_TRUSTED_ORIGINS = ['http://192.168.1.154:8000','http://143.198.102.57:3000','http://192.168.1.78:3000' ]
# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

AUTH_USER_MODEL = 'accounts.User'  


REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': (
         'rest_framework_simplejwt.authentication.JWTAuthentication', 
     ),
     'DEFAULT_PERMISSION_CLASSES': (
         'rest_framework.permissions.IsAuthenticated',
         'rest_framework.permissions.AllowAny',
     ),
     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
     'PAGE_SIZE': 10,
     'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
 }

#JWT authentication is enabled
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24), 
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  
    'ROTATE_REFRESH_TOKENS': True,  
    'BLACKLIST_AFTER_ROTATION': True,  
    'AUTH_HEADER_TYPES': ('Bearer',),  
    'USER_ID_FIELD': 'id',  
    'USER_ID_CLAIM': 'user_id', 
    'SIGNING_KEY': SECRET_KEY,  
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_URL = '/static/'

CKEDITOR_RESTRICT_BY_USER = False
CKEDITOR_REQUIRE_STAFF = False
CKEDITOR_ALLOW_NONIMAGE_FILES = False

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',
            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}