DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'roki',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '54.176.123.132',
        'PORT': 3306,
    }
}

REDIS = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://54.176.123.132:6379/1",
    }
}
