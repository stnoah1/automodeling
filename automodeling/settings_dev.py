try:
    from .settings import *
except ImportError:
    pass

INSTALLED_APPS += ['debug_toolbar',]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
