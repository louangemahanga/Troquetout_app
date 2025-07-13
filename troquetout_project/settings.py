

from pathlib import Path
import os 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mb=jgsg*6)-8#)d#n%r%b!zs%+lpcabjpv!v=so!hhg$!1pw7!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
APPEND_SLASH = True # Assurez-vous que cette ligne est présente et True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'troquetout_app',
    'widget_tweaks',
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

ROOT_URLCONF = 'troquetout_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[BASE_DIR / 'troquetout_app' / 'templates'],
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

WSGI_APPLICATION = 'troquetout_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Chemin pour trouver tes fichiers statiques dans les apps
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), # Si tu as un dossier 'static' à la racine de ton projet
]

# Pour la production, où Django va collecter tous les statiques
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# troquetout_project/settings.py

# ... (le reste de vos settings) ...

# Configuration des redirections d'authentification
LOGIN_REDIRECT_URL = 'home' # Redirige vers la page d'accueil après la connexion

LOGOUT_REDIRECT_URL = 'home' # Redirige vers la page d'accueil après la déconnexion

# LOGOUT_URL= 'logout'
LOGIN_URL = 'login' # Nom de l'URL pour la page de connexion (utilisé par @login_required)

# troquetout_project/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.tonfournisseur.com' # Ex: smtp.gmail.com, smtp.mail.yahoo.com
EMAIL_PORT = 587 # Généralement 587 pour TLS ou 465 pour SSL
EMAIL_USE_TLS = True # Utilise True pour la plupart des serveurs modernes
# EMAIL_USE_SSL = False # Si tu utilises SSL (port 465), mets True ici et False pour EMAIL_USE_TLS
EMAIL_HOST_USER = 'ton_adresse_email_expediteur@example.com' # Ton adresse email pour envoyer
EMAIL_HOST_PASSWORD = 'ton_mot_de_passe_email' # Le mot de passe de cet email
DEFAULT_FROM_EMAIL = 'ne-pas-repondre@troquetout.com' # L'adresse par défaut qui apparaîtra comme expéditeur