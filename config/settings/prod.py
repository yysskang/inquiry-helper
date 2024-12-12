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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = secrets.secret_data("email_host")
EMAIL_USE_TLS = True
EMAIL_PORT = secrets.secret_data("email_port")
EMAIL_HOST_USER = secrets.secret_data("email_user")
EMAIL_HOST_PASSWORD = secrets.secret_data("email_password")

