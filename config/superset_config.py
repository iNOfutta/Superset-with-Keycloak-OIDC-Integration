import os
import sys
sys.path.append('/app/config')
from keycloak_security_manager import OIDCSecurityManager
from flask_appbuilder.security.manager import AUTH_OID


# Environment Configuration
ENV = os.environ.get('FLASK_ENV', 'production')
DEBUG = ENV == 'development'

# Authentication Configuration
AUTH_TYPE = AUTH_OID
SECRET_KEY = os.environ.get('SECRET_KEY', 'temporary-secret-key')
OIDC_CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secret.json')
CUSTOM_SECURITY_MANAGER = OIDCSecurityManager

# For production, running behind nginx reverse proxy
ENABLE_PROXY_FIX = os.environ.get('ENABLE_PROXY_FIX', False)
OIDC_REDIRECT_URI = os.environ.get('OIDC_REDIRECT_URI', 'http:localhost:8088')

PREFERRED_URL_SCHEME = os.environ.get('PREFERRED_URL_SCHEME', 'http')

# User Registration
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = os.environ.get('DEFAULT_USER_REGISTRATION_ROLE', 'Gamma')

# Database Configuration
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://superset:superset@host.docker.internal:3306/superset')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 1800
}

# Redis Configuration
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')
REDIS_DB = int(os.environ.get('REDIS_DB', '0'))
REDIS_URL = f"redis://{f':{REDIS_PASSWORD}@' if REDIS_PASSWORD else ''}{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# Cache Configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_URL': REDIS_URL
}

# Feature Flags
FEATURE_FLAGS = {
    "DASHBOARD_CACHE": True,
    "ENABLE_JAVASCRIPT_CONTROLS": True,
    "DASHBOARD_NATIVE_FILTERS_SET": True,  # Faster dashboard filters
    "DASHBOARD_CROSS_FILTERS": True  # Enable cross filtering
}

# Role Mapping
AUTH_ROLES_MAPPING = {
    'Admin': ['Admin', 'admin', 'ADMIN', 'realm-admin', 'realm:admin'],
    'Alpha': ['Alpha', 'alpha'],
    'Gamma': ['Gamma', 'gamma'],
    'Public': ['Public', 'public']
}

# Security Settings
WTF_CSRF_ENABLED = False


# Logging Configuration
if DEBUG:
    # Development logging - detailed in-app logs
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s:%(levelname)s:%(name)s:%(message)s',
            },
            'werkzeug': {
                'format': '%(asctime)s %(levelname)s %(message)s [in %(pathname)s:%(lineno)d]',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout',
            },
            'werkzeug_console': {
                'class': 'logging.StreamHandler',
                'formatter': 'werkzeug',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            'superset': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'flask_appbuilder': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'werkzeug': {
                'handlers': ['werkzeug_console'],
                'level': 'INFO',
                'propagate': False,
            },
            'keycloak': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'flask_oidc': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
else:
    # Production logging - only important logs
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s:%(levelname)s:%(name)s:%(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            'superset': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True,
            },
            'flask_appbuilder': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True,
            },
            'werkzeug': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
