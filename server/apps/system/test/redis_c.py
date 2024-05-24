# -*- coding:utf-8 -*-
from utils.client import publish_message

if __name__ == "__main__":
    # 测试发布订阅
    channel = 'my_channel'
    publish_message(channel, 999)
