DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "roki",
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": "192.168.87.21",
        "PORT": 3306,
    }
}

REDIS = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://192.168.87.21:6379/1",
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
            "host": "192.168.87.21",
            "port": 27017,
            "authSource": "admin",
            "authMechanism": "SCRAM-SHA-256",
            "maxPoolSize": 32
        }
    }
}
