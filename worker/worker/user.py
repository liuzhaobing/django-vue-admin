# -*- coding:utf-8 -*-
import time
import json
import logging
import threading

import urllib3
from . import mongo_db
from .conf import MANAGER
from .manager import TaskManager, TaskPlan, TaskStatus
from .metrics import *
from .tasks import publish_case, get_case, get_cases_count
from utils.data import *

logger = logging.getLogger("log")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NLPUser:
    def __init__(self, task: TaskManager, plan: TaskPlan, *args, **kwargs):
        self.task = task
        self.plan = plan
        self.cases_count = 0

    def prepare(self, *args, **kwargs):
        """准备测试用例"""
        self.task.prepare(*args, **kwargs)

        self.cases_count = get_cases_count(self.task.job_instance_id)
        if self.cases_count != 0:
            return

        self.plan.config = json.loads(self.plan.config) if self.plan.config else {
            "address": "https://speech.myroki.com/dds/v3/test3",
            "chan_num": 1
        }

        self.plan.data_source = json.loads(self.plan.data_source) if self.plan.data_source else {
            "type": "xlsx",
            "file": {"file_name": "/media/2024/05/20/老板电器-思必驰标准测试集-new.xlsx", "sheet_name": "Sheet1"},
        }

        if self.plan.data_source["type"] == "xlsx":
            filename = self.plan.data_source["file"]["file_name"].removeprefix("/")
            df = pd.read_excel(io=filename,
                               sheet_name=self.plan.data_source["file"]["sheet_name"])
            for index, line in enumerate(df.values):
                publish_case(self.task.job_instance_id,
                             json.dumps(dict(zip(list(df.columns), line)), ensure_ascii=False))
                self.cases_count = index + 1

    def extract_nlp_output(self, msg: dict) -> dict | None:
        """extract key information from output log"""
        try:
            result = {
                "act_question": msg["dm"]["input"],
                "act_domain": msg["skill"],
                "act_intent": msg["dm"].get("intentName", ""),
                "act_slots": {},
                "answer_string": msg["dm"]["nlg"],
                "session_id": msg["sessionId"],
                "trace_id": msg["recordId"],
            }
            if "semantics" in msg["nlu"]:
                result["act_slots"] = {item["name"]: item["value"]
                                       for item in msg["nlu"]["semantics"]["request"]["slots"] if
                                       item["name"] != "intent"}
            return result
        except Exception as e:
            return None

    def call_interface(self, row: dict):
        params = {
            "serviceType": "websocket",
            "communicationType": "fullDuplex",
            "deviceName": "DUI001",
            "productId": "279607021",
        }
        payload = {
            "topic": "nlu.input.text",
            "refText": row["question"],
            "recordId": generate_trace_id(self.task.type_name_en),
            "sessionId": row.get("session_id") if row.get("session_id") else generate_trace_id(self.task.type_name_en),
        }

        start_time = time.perf_counter()
        response = requests.post(
            url=self.plan.config["address"],
            params=params,
            json=payload,
            verify=False,
        )
        end_time = time.perf_counter()
        row["edg_cost"] = round((end_time - start_time) * 1000)
        logger.info(response.text)
        try:
            result = self.extract_nlp_output(response.json())
            result["is_intent_pass"] = result["act_intent"] == row["intent"]
            result["act_slots"] = json.dumps(result["act_slots"], ensure_ascii=False) if result["act_slots"] else ""
        except Exception as e:
            print(e)
        return {**row, **result}

    def calculate_slots_acc(self, slots: dict | str, act_slots: dict | str):
        slots = json.loads(slots) if not isinstance(slots, dict) else slots
        act_slots = json.loads(act_slots) if not isinstance(act_slots, dict) else act_slots
        return slots == act_slots

    def get_slots_metrics(self, results: list[dict]):
        pass_count = sum(
            map(lambda item: self.calculate_slots_acc(item["slots"], item["act_slots"]), results)
        )
        return pass_count / self.cases_count

    def calculate_nlp_metrics(
            self,
            results: list[dict],
            metrics: list[Callable] = [f1_score, precision_score, recall_score]
    ):
        """calculate metrics"""
        macro_domain = get_metrics(results, "domain", "act_domain", metrics, average="macro")
        micro_domain = get_metrics(results, "domain", "act_domain", metrics, average="micro")
        domain_metrics = get_metrics(results, "domain", "act_domain", metrics)
        macro_intent = get_metrics(results, "intent", "act_intent", metrics, average="macro")
        micro_intent = get_metrics(results, "intent", "act_intent", metrics, average="micro")
        intent_metrics = get_metrics(results, "intent", "act_intent", metrics)
        return macro_domain + micro_domain + macro_intent + micro_intent, domain_metrics, intent_metrics

    def start_running(self, *args, **kwargs):
        """执行测试用例"""
        self.task.running(*args, **kwargs)

        def run_one_case(case_info: dict | str):
            case_info["job_instance_id"] = self.task.job_instance_id
            one_result = self.call_interface(case_info)
            mongo_db[self.task.type_name_en].insert_one(one_result)
            logger.info(one_result)
            return one_result

        def one_user_running():
            while True:
                if self.task.context.done():
                    return None
                case = get_case(self.task.job_instance_id)
                if case is None:
                    return None
                run_one_case(json.loads(case))
                reset_count = get_cases_count(self.task.job_instance_id)
                progress = f"{self.cases_count - reset_count}/{self.cases_count}"
                self.task.update_progress(progress)
                progress_percent = int((self.cases_count - reset_count) * 100 / self.cases_count)
                self.task.update_progress_percent(progress_percent)

        users = []
        for i in range(self.plan.config["chan_num"]):
            u = threading.Thread(target=one_user_running)
            u.daemon = True
            u.start()
            users.append(u)

        [u.join() for u in users]
        logger.info("start_running execute finished!")

    def success(self, *args, **kwargs):
        log_all_data = mongo_db[self.task.type_name_en].find({"job_instance_id": self.task.job_instance_id},
                                                             {"_id": 0})
        log_headers = [{"key": "id", "label": "用例编号"}, {"key": "question", "label": "测试语句"},
                       {"key": "domain", "label": "期望domain"}, {"key": "act_domain", "label": "实际domain"},
                       {"key": "intent", "label": "期望intent"}, {"key": "act_intent", "label": "实际intent"},
                       {"key": "is_intent_pass", "label": "意图是否通过"}, {"key": "slots", "label": "槽位期望值"},
                       {"key": "act_slots", "label": "槽位实际值"}, {"key": "is_slots_pass", "label": "槽位是否通过"},
                       {"key": "is_pass", "label": "是否通过"}, {"key": "edg_cost", "label": "端侧耗时(ms)"},
                       {"key": "answer_string", "label": "回答内容"}, {"key": "device_id", "label": "DeviceId"},
                       {"key": "session_id", "label": "SessionId"}, {"key": "trace_id", "label": "TranceId"}]
        log_all_data_format = format_log_details(log_headers, log_all_data)

        overall, domain_metrics, intent_metrics = self.calculate_nlp_metrics(log_all_data)

        report_headers = [{"key": "precision_score", "label": "精确率"}, {"key": "recall_score", "label": "召回率"},
                          {"key": "f1_score", "label": "F1"}, {"key": "average", "label": "指标"},
                          {"key": "domain", "label": "领域"}, {"key": "intent", "label": "意图"}]

        report_all_data_format = format_log_details(report_headers, overall + domain_metrics + intent_metrics)

        filename = write_excel_file(f"logs/{self.task.job_instance_id}.xlsx",
                                    测试报告=report_all_data_format, 测试日志=log_all_data_format)
        remote_filename = upload_file(filename, f"{MANAGER}/api/test/file/")

        if self.task.status == TaskStatus.RUNNING:
            if self.task.progress_percent in [100, "100"]:
                self.task.success(result_file=remote_filename)
            else:
                self.task.failure("用例执行完毕, 但是进度未达到100%, 请检查!")


__all__ = (
    'NLPUser',
)