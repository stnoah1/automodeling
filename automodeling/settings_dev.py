try:
    from .settings import *
except ImportError:
    pass

INSTALLED_APPS += ['debug_toolbar', 'recognize',]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
BROKER_BACKEND = 'memory'
INTERNAL_IPS = ['127.0.0.1', '192.168.1.59']

ALLOWED_HOSTS = ['localhost:8000', '*']
