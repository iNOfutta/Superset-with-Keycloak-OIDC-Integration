import os
import sys
sys.path.append('/app/config')
from keycloak_security_manager import OIDCSecurityManager
from flask_appbuilder.security.manager import AUTH_OID

# Internationalization Configuration
BABEL_DEFAULT_LOCALE = os.environ.get('BABEL_DEFAULT_LOCALE', 'en')
LANGUAGES = {
    'en': {'flag': 'us', 'name': 'English'},
    'es': {'flag': 'es', 'name': 'Spanish'},
    'it': {'flag': 'it', 'name': 'Italian'},
    'fr': {'flag': 'fr', 'name': 'French'},
    'zh': {'flag': 'cn', 'name': 'Chinese'},
    'ja': {'flag': 'jp', 'name': 'Japanese'},
    'de': {'flag': 'de', 'name': 'German'},
    'pt': {'flag': 'pt', 'name': 'Portuguese'},
    'pt_BR': {'flag': 'br', 'name': 'Brazilian Portuguese'},
    'ru': {'flag': 'ru', 'name': 'Russian'},
    'ko': {'flag': 'kr', 'name': 'Korean'},
    'sk': {'flag': 'sk', 'name': 'Slovak'},
    'sl': {'flag': 'si', 'name': 'Slovenian'},
    'nl': {'flag': 'nl', 'name': 'Dutch'},
    'sv': {'flag': 'se', 'name': 'Swedish'},
    'tr': {'flag': 'tr', 'name': 'Turkish'},
    'ga': {'flag': 'ie', 'name': 'Irish'},
    'pl': {'flag': 'pl', 'name': 'Polish'},
    'vi': {'flag': 'vn', 'name': 'Vietnamese'},
    'el': {'flag': 'gr', 'name': 'Greek'},
    'no': {'flag': 'no', 'name': 'Norwegian'},
    'th': {'flag': 'th', 'name': 'Thai'},
    'uk': {'flag': 'ua', 'name': 'Ukrainian'},
    'he': {'flag': 'il', 'name': 'Hebrew'},
    'id': {'flag': 'id', 'name': 'Indonesian'},
    'da': {'flag': 'dk', 'name': 'Danish'},
    'fi': {'flag': 'fi', 'name': 'Finnish'},
    'hu': {'flag': 'hu', 'name': 'Hungarian'},
    'hi': {'flag': 'in', 'name': 'Hindi'},
    'cs': {'flag': 'cz', 'name': 'Czech'},
    'ro': {'flag': 'ro', 'name': 'Romanian'},
    'ca': {'flag': 'ca', 'name': 'Catalan'},
    'bn': {'flag': 'bd', 'name': 'Bengali'},
    'ar': {'flag': 'sa', 'name': 'Arabic'},
    'ms': {'flag': 'my', 'name': 'Malay'},
    'bg': {'flag': 'bg', 'name': 'Bulgarian'},
    'hr': {'flag': 'hr', 'name': 'Croatian'},
    'lt': {'flag': 'lt', 'name': 'Lithuanian'},
    'sr': {'flag': 'rs', 'name': 'Serbian'},
    'et': {'flag': 'ee', 'name': 'Estonian'},
    'lv': {'flag': 'lv', 'name': 'Latvian'},
    'gl': {'flag': 'gl', 'name': 'Galician'},
    'af': {'flag': 'za', 'name': 'Afrikaans'},
    'sw': {'flag': 'ke', 'name': 'Swahili'},
    'ta': {'flag': 'in', 'name': 'Tamil'},
    'te': {'flag': 'in', 'name': 'Telugu'},
    'kn': {'flag': 'in', 'name': 'Kannada'},
    'ml': {'flag': 'in', 'name': 'Malayalam'},
    'gu': {'flag': 'in', 'name': 'Gujarati'},
    'pa': {'flag': 'in', 'name': 'Punjabi'},
    'mr': {'flag': 'in', 'name': 'Marathi'},
    'ne': {'flag': 'np', 'name': 'Nepali'},
    'si': {'flag': 'lk', 'name': 'Sinhala'},
    'km': {'flag': 'kh', 'name': 'Khmer'},
    'lo': {'flag': 'la', 'name': 'Lao'},
    'my': {'flag': 'mm', 'name': 'Burmese'},
    'ka': {'flag': 'ge', 'name': 'Georgian'},
    'am': {'flag': 'et', 'name': 'Amharic'},
    'kk': {'flag': 'kz', 'name': 'Kazakh'},
    'ky': {'flag': 'kg', 'name': 'Kyrgyz'},
    'tg': {'flag': 'tj', 'name': 'Tajik'},
    'tk': {'flag': 'tm', 'name': 'Turkmen'},
    'uz': {'flag': 'uz', 'name': 'Uzbek'},
    'mn': {'flag': 'mn', 'name': 'Mongolian'},
    'ps': {'flag': 'af', 'name': 'Pashto'},
    'ku': {'flag': 'iq', 'name': 'Kurdish'},
    'bo': {'flag': 'cn', 'name': 'Tibetan'},
    'ug': {'flag': 'cn', 'name': 'Uyghur'},
    'dz': {'flag': 'bt', 'name': 'Dzongkha'},
    'jw': {'flag': 'id', 'name': 'Javanese'},
    'su': {'flag': 'id', 'name': 'Sundanese'},
    'ceb': {'flag': 'ph', 'name': 'Cebuano'},
    'fil': {'flag': 'ph', 'name': 'Filipino'},
    'hmn': {'flag': 'cn', 'name': 'Hmong'},
    'haw': {'flag': 'us', 'name': 'Hawaiian'},
    'mi': {'flag': 'nz', 'name': 'Maori'},
    'sm': {'flag': 'ws', 'name': 'Samoan'},
    'to': {'flag': 'to', 'name': 'Tongan'},
    'fj': {'flag': 'fj', 'name': 'Fijian'},
    'ty': {'flag': 'pf', 'name': 'Tahitian'},
    'mg': {'flag': 'mg', 'name': 'Malagasy'},
    'yo': {'flag': 'ng', 'name': 'Yoruba'},
    'ig': {'flag': 'ng', 'name': 'Igbo'},
    'sn': {'flag': 'zw', 'name': 'Shona'},
    'zu': {'flag': 'za', 'name': 'Zulu'},
    'xh': {'flag': 'za', 'name': 'Xhosa'},
    'st': {'flag': 'za', 'name': 'Sotho'},
    'tn': {'flag': 'bw', 'name': 'Tswana'},
    'ss': {'flag': 'sz', 'name': 'Swati'},
    've': {'flag': 'za', 'name': 'Venda'},
    'ts': {'flag': 'za', 'name': 'Tsonga'},
    'nr': {'flag': 'za', 'name': 'Ndebele'},
    'ff': {'flag': 'sn', 'name': 'Fula'},
    'wo': {'flag': 'sn', 'name': 'Wolof'},
    'so': {'flag': 'so', 'name': 'Somali'},
    'ha': {'flag': 'ng', 'name': 'Hausa'},
    'sw': {'flag': 'ke', 'name': 'Swahili'},
    'rw': {'flag': 'rw', 'name': 'Kinyarwanda'},
    'ny': {'flag': 'mw', 'name': 'Chichewa'},
    'sn': {'flag': 'zw', 'name': 'Shona'},
    'zu': {'flag': 'za', 'name': 'Zulu'},
    'xh': {'flag': 'za', 'name': 'Xhosa'},
    'st': {'flag': 'za', 'name': 'Sotho'},
    'tn': {'flag': 'bw', 'name': 'Tswana'},
    'ss': {'flag': 'sz', 'name': 'Swati'},
    've': {'flag': 'za', 'name': 'Venda'},
    'ts': {'flag': 'za', 'name': 'Tsonga'},
    'nr': {'flag': 'za', 'name': 'Ndebele'},
    'ff': {'flag': 'sn', 'name': 'Fula'},
    'wo': {'flag': 'sn', 'name': 'Wolof'},
    'so': {'flag': 'so', 'name': 'Somali'},
    'ha': {'flag': 'ng', 'name': 'Hausa'},
    'sw': {'flag': 'ke', 'name': 'Swahili'},
    'rw': {'flag': 'rw', 'name': 'Kinyarwanda'},
    'ny': {'flag': 'mw', 'name': 'Chichewa'},
}

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
