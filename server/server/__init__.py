# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
import redis
import pymongo
import pymysql
from .celery import app as celery_app
from .conf import MONGO, REDIS

pymysql.install_as_MySQLdb()
mongo_client = pymongo.MongoClient(**MONGO['default']['CLIENT'])
mongo_db = mongo_client[MONGO['default']['NAME']]
redis_pool = redis.ConnectionPool.from_url(REDIS['default']['LOCATION'])

__all__ = (
    'celery_app',
    'mongo_client',
    'mongo_db',
    'redis_pool',
)
