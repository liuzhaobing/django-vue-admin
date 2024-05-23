# -*- coding:utf-8 -*-
import redis

from server import redis_pool


def publish_message(channel, message):
    """发布消息到频道"""
    redis_client = redis.StrictRedis(connection_pool=redis_pool)
    return redis_client.publish(channel, message)


def subscribe_channel(channel) -> str:
    """订阅频道，并处理接收到的消息"""
    redis_client = redis.StrictRedis(connection_pool=redis_pool)
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        if message['type'] == 'message':
            yield message['data'].decode('utf-8')


def get_channel_history(channel):
    """获取频道的消息历史记录"""
    redis_client = redis.StrictRedis(connection_pool=redis_pool)
    # 获取频道历史记录列表
    history = redis_client.lrange(f"{channel}_history", 0, -1)
    # 将字节转换为字符串并返回历史记录列表
    return [message.decode('utf-8') for message in history]


def push_to_queue(queue_name, message):
    """推入消息到队列"""
    redis_client = redis.StrictRedis(connection_pool=redis_pool)
    return redis_client.lpush(queue_name, message)


def pop_from_queue(queue_name) -> str | None:
    """从队列中弹出消息"""
    redis_client = redis.StrictRedis(connection_pool=redis_pool)
    message = redis_client.rpop(queue_name)
    return message.decode('utf-8') if message else None


def get_queue_elements(queue_name):
    """获取队列中的所有元素"""
    redis_client = redis.StrictRedis(connection_pool=redis_pool)
    return [row.decode('utf-8') for row in redis_client.lrange(queue_name, 0, -1)]


def hash_set(key, field, value):
    """设置哈希表字段的值"""
    redis_client = redis.StrictRedis(connection_pool=redis_pool)
    return redis_client.hset(key, field, value)


def hash_get(key, field) -> str | None:
    """获取哈希表字段的值"""
    redis_client = redis.StrictRedis(connection_pool=redis_pool)
    value = redis_client.hget(key, field)
    return value.decode() if value else None


def hash_get_all(key):
    """获取哈希表所有字段的值"""
    redis_client = redis.StrictRedis(connection_pool=redis_pool)
    values = redis_client.hgetall(key)
    return {key.decode(): value.decode() for key, value in values.items()} if values else None


def hash_delete_key(key, *keys):
    """删除哈希表字段的值"""
    redis_client = redis.StrictRedis(connection_pool=redis_pool)
    return redis_client.hdel(key, *keys)


def hash_delete_table(key):
    """删除哈希表"""
    redis_client = redis.StrictRedis(connection_pool=redis_pool)
    return redis_client.delete(key)
