# -*- coding:utf-8 -*-
from utils.client import subscribe_channel, publish_message

if __name__ == "__main__":
    # 测试发布订阅
    channel = 'my_channel'
    for message in subscribe_channel(channel):
        print(message)
