import os

import requests
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
TOKEN_VALIDITY_SECS = int(os.getenv('TOKEN_VALIDITY_SECS', '3600'))


def redis_uri():
    return os.getenv('REDIS_URI', 'redis://localhost:6379/0')


def database_uri():
    return os.getenv('DATABASE_URI')


def base_url():
    return os.getenv('BASE_URL', 'http://127.0.0.1:5000')


def init_app(app: Flask):
    app.secret_key = os.getenvb(b"SECRET_KEY") or os.urandom(24)

    app.config.update(
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI=database_uri(),
        REDIS_URL=redis_uri(),
        GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID"),
        GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET"),
        GOOGLE_PROVIDER_CONFIG=requests.get(GOOGLE_DISCOVERY_URL).json(),
        BASE_URL=base_url(),
    )


def storage_base_url():
    return os.getenv('STORAGE_BASE_URL', base_url()).rstrip('/')


def s3_settings():
    return {
        'BUCKET': os.getenv('S3_BUCKET'),
        'HOST': os.getenv('S3_HOST'),
        'ACCESS_KEY': os.getenv('S3_ACCESS_KEY'),
        'SECRET_KEY': os.getenv('S3_SECRET_KEY'),
        'SECURE': bool(os.getenv('S3_SECURE', 'False')),
    }
