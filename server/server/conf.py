from utils.data import read_yaml_file

DEBUG = False
config = read_yaml_file("conf/config.yaml")
DATABASES = config["mysql-roki"]
REDIS = config["redis-roki"]
MONGO = config["mongo-roki"]
MANAGER = config["manager"]

__all__ = (
    "DATABASES",
    "REDIS",
    "MONGO",
    "MANAGER",
)
