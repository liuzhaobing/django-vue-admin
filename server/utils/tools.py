# -*- coding:utf-8 -*-
import os
import base64
import datetime


def generate_trace_id(tp: str = "LLM"):
    now = datetime.datetime.now()
    return tp.upper() + now.strftime("%Y%m%d%H%M%S") + base64.b32encode(os.urandom(5)).decode("ascii")
