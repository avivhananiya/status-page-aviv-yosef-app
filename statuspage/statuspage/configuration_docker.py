"""
Docker / Kubernetes configuration module.

Reads all required settings from environment variables injected by:
  - K8s ConfigMap  (non-sensitive: DB_HOST, REDIS_HOST, ports, etc.)
  - K8s Secrets    (sensitive: DB_PASSWORD, REDIS_PASSWORD, DJANGO_SECRET_KEY)

This file replaces the local-only configuration.py (which is gitignored)
and is used in CI, Docker containers, and production pods.
"""

import os

# -------------------------------------------------------
# Required Settings
# -------------------------------------------------------

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

DATABASE = {
    'NAME': os.environ.get('DB_NAME', 'statuspage'),
    'USER': os.environ.get('DB_USER', 'statuspage'),
    'PASSWORD': os.environ.get('DB_PASSWORD', ''),
    'HOST': os.environ.get('DB_HOST', 'localhost'),
    'PORT': os.environ.get('DB_PORT', '5432'),
    'CONN_MAX_AGE': int(os.environ.get('DB_CONN_MAX_AGE', '300')),
}

REDIS = {
    'tasks': {
        'HOST': os.environ.get('REDIS_HOST', 'localhost'),
        'PORT': int(os.environ.get('REDIS_PORT', '6379')),
        'PASSWORD': os.environ.get('REDIS_PASSWORD', ''),
        'DATABASE': int(os.environ.get('REDIS_DB_TASKS', '0')),
        'SSL': os.environ.get('REDIS_SSL', 'False').lower() in ('true', '1', 'yes'),
    },
    'caching': {
        'HOST': os.environ.get('REDIS_HOST', 'localhost'),
        'PORT': int(os.environ.get('REDIS_PORT', '6379')),
        'PASSWORD': os.environ.get('REDIS_PASSWORD', ''),
        'DATABASE': int(os.environ.get('REDIS_DB_CACHE', '1')),
        'SSL': os.environ.get('REDIS_SSL', 'False').lower() in ('true', '1', 'yes'),
    },
}

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')

SITE_URL = os.environ.get('SITE_URL', '').strip()

# -------------------------------------------------------
# Optional Settings
# -------------------------------------------------------

BASE_PATH = os.environ.get('BASE_PATH', '')

DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

LOGIN_TIMEOUT = int(os.environ.get('LOGIN_TIMEOUT', '1209600'))

TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')

RQ_DEFAULT_TIMEOUT = int(os.environ.get('RQ_DEFAULT_TIMEOUT', '300'))

CORS_ORIGIN_ALLOW_ALL = os.environ.get('CORS_ORIGIN_ALLOW_ALL', 'False').lower() in ('true', '1', 'yes')

_cors_whitelist = os.environ.get('CORS_ORIGIN_WHITELIST', '').strip()
CORS_ORIGIN_WHITELIST = [u for u in _cors_whitelist.split(',') if u] if _cors_whitelist else []

PLUGINS = []
_plugins = os.environ.get('PLUGINS', '').strip()
if _plugins:
    PLUGINS = [p.strip() for p in _plugins.split(',') if p.strip()]
