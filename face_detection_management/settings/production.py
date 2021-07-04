import dj_database_url
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY') # 環境変数に用意

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'face_detection_management',
        'USER': os.environ.get('DB_USER'), # 環境変数に用意
        'PASSWORD': os.environ.get('DB_PASSWORD'), # 環境変数に用意
        'HOST': 'localhost',
        'PORT': '',
    }
}
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)