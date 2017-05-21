try:
    from .settings import *
except ImportError:
    pass

INSTALLED_APPS += ['debug_toolbar', 'recognize',]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
