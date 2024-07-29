from .base import *
ALLOWED_HOSTS = ["*"]
DEBUG = False

import pymysql
pymysql.install_as_MySQLdb()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': secrets.secret_data("DB_HOST"),
        'PORT': 3306,
        'NAME': secrets.secret_data("DB_NAME"),
        'USER': secrets.secret_data("DB_USER"),
        'PASSWORD': secrets.secret_data("DB_PASSWORD"),
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
        },
    }
}

