# -*- coding:utf-8 -*-
import logging

import yaml
import requests
from openpyxl import Workbook

logger = logging.getLogger("log")


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
    return filename
