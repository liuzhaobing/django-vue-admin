# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
import pymongo
import pymysql
from .celery import app as celery_app
from .conf import MONGO

pymysql.install_as_MySQLdb()
mongo_client = pymongo.MongoClient(**MONGO['default']['CLIENT'])
mongo_db = mongo_client[MONGO['default']['NAME']]

__all__ = (
    'celery_app',
    'mongo_client',
    'mongo_db',
)
