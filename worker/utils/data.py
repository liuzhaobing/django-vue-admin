# -*- coding:utf-8 -*-
import base64
import datetime
import logging
import math
import os

import yaml
import requests
import pandas as pd
from openpyxl import Workbook

logger = logging.getLogger("log")


def process_nan(content):
    if isinstance(content, float):
        if math.isnan(content):
            return ""
    return content


def generate_job_instance_id(tp: str = "LLM"):
    now = datetime.datetime.now()
    return tp.upper() + now.strftime("%Y%m%d%H%M%S") + base64.b32encode(os.urandom(5)).decode("ascii")


def generate_trace_id(tp: str = "LLM"):
    return generate_job_instance_id(tp) + "@myroki-test.com"


def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        logger.info(f"Reading yaml file {file_path}")
        return yaml.safe_load(file)


def upload_file(file_path, upload_url) -> str | None:
    try:
        with open(file_path, "rb") as file:
            response = requests.post(upload_url, files={"file": file})
            if response.status_code == 200:
                logger.info("文件上传成功！")
                return response.json()["data"]["path"]
            else:
                logger.error(f"文件上传失败server: {response.text}")
                return None
    except Exception as e:
        logger.error(f"文件上传失败client: {e}")
    return None


def format_log_details(headers: list[dict], datas: list[dict]):
    """
    headers = [{"key": "id", "label": "用例编号"}, {"key": "question", "label": "测试语句"},
               {"key": "domain", "label": "期望domain"}, {"key": "act_domain", "label": "实际domain"},
               {"key": "intent", "label": "期望intent"}, {"key": "act_intent", "label": "实际intent"},
               {"key": "is_intent_pass", "label": "意图是否通过"}, {"key": "slots", "label": "槽位期望值"},
               {"key": "act_slots", "label": "槽位实际值"}, {"key": "is_slots_pass", "label": "槽位是否通过"},
               {"key": "is_pass", "label": "是否通过"}, {"key": "edg_cost", "label": "端侧耗时(ms)"},
               {"key": "answer_string", "label": "回答内容"}, {"key": "device_id", "label": "DeviceId"},
               {"key": "session_id", "label": "SessionId"}, {"key": "trace_id", "label": "TranceId"}]
    datas = [
        {"id": 1, "question": "今天下雨吗", "domain": "weather", "act_domain": "weather", "intent": "GetWeather",
         "act_intent": "GetWeather", "is_intent_pass": True, "slots": "{\"日期\":\"今天\"}",
         "act_slots": "{\"日期\":\"今天\"}", "is_slots_pass": True,
         "is_pass": True, "edg_cost": 0, "answer_string": "今天天气晴朗", "device_id": "123456789",
         "session_id": "123456789", "trace_id": "123456789"},
        {"id": 2, "question": "明天下雨吗", "domain": "weather", "act_domain": "weather", "intent": "GetWeather",
         "act_intent": "GetWeather", "is_intent_pass": True, "slots": "{\"日期\":\"明天\"}",
         "act_slots": "{\"日期\":\"明天\"}", "is_slots_pass": True,
         "is_pass": True, "edg_cost": 0, "answer_string": "明天天气晴朗", "device_id": "123456789",
         "session_id": "123456789", "trace_id": "123456789"},
    ]
    :param headers:
    :param datas:
    :return:
    """
    return [[h["label"] for h in headers]] + [[data.get(header["key"], "") for header in headers] for data in datas]


def write_excel_file(filename: str, **kwargs):
    wb = Workbook()
    wb.remove(wb["Sheet"])
    for key, values in kwargs.items():
        ws = wb.create_sheet(key)
        [ws.append(row) for row in values]
    wb.save(filename)
    logger.info(f"Excel file {filename} created")
    return filename


def load_data_from_xlsx(filename: str, sheet_name: str, **kwargs) -> list[dict]:
    """从excel中读取数据为JSON格式的对象
    Parameters
    ----------

    filename : str
        /home/download/xxx.xlsx
    sheet_name : str
        Sheet1

        | id   | text_1                    | text_2                 |
        | ---- | ------------------ ------ | --------------------- |
        | 1    | 后面的那几个机器人是你的朋友吗 | 后面的机器人是你的朋友吗   |
        | 2    | 后面的那几个机器人是你的朋友吗 | 你的机器人朋友是谁       |
        | 3    | 后面的那几个机器人是你的朋友吗 | 那坏人是你的朋友吗       |
        | 4    | 后面的那几个机器人是你的朋友吗 | 你们的朋友都是机器人吗   |

    Returns
    -------
    list[dict]
        [{"id": 1, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "后面的机器人是你的朋友吗"},
         {"id": 2, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你的机器人朋友是谁"},
         {"id": 3, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "那坏人是你的朋友吗"},
         {"id": 4, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你们的朋友都是机器人吗"}]
    """
    df = pd.read_excel(io=filename, sheet_name=sheet_name, **kwargs)
    return [dict(zip(list(df.columns), line)) for line in df.values]
