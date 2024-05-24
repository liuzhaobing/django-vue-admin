# -*- coding:utf-8 -*-
import redis
import pymongo
from .conf import MONGO, REDIS

mongo_client = pymongo.MongoClient(**MONGO['default']['CLIENT'])
mongo_db = mongo_client[MONGO['default']['NAME']]
redis_pool = redis.ConnectionPool.from_url(REDIS['default']['LOCATION'])

__all__ = (
    'mongo_client',
    'mongo_db',
    'redis_pool',
)
