DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "roki",
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": "54.176.123.132",
        "PORT": 3306,
    }
}

REDIS = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://54.176.123.132:6379/1",
    }
}

MONGO = {
    "default": {
        "ENGINE": "djongo",
        "NAME": "roki",
        "ENFORCE_SCHEMA": False,
        "CLIENT": {
            "username": "root",
            "password": "123456",
            "host": "54.176.123.132",
            "port": 27017,
            "authSource": "admin",
            "authMechanism": "SCRAM-SHA-256",
            "maxPoolSize": 32
        }
    }
}
