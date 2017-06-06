try:
    from .settings import *
except ImportError:
    pass

ALLOWED_HOSTS += ['ec2-52-78-86-158.ap-northeast-2.compute.amazonaws.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'hwang.cgo5b9prqnhl.ap-northeast-2.rds.amazonaws.com',
        'NAME': 'automodel',
        'USER': 'hwanght1',
        'PASSWORD': 'gusxo123',
    },
}
