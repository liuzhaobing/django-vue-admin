# -*- coding:utf-8 -*-
import json
import logging
import threading
import time

from .manager import TaskManager, TaskPlan
from .tasks import publish_case, get_case, get_cases_count

logger = logging.getLogger("log")


class NLPUser:
    def __init__(self, task: TaskManager, plan: TaskPlan, *args, **kwargs):
        self.task = task
        self.plan = plan

    def prepare(self, *args, **kwargs):
        """准备测试用例"""
        self.cases_count = 1000
        [publish_case(self.task.job_instance_id, json.dumps({"id": i}, ensure_ascii=False))
         for i in range(self.cases_count)]

    def start_running(self, *args, **kwargs):
        """执行测试用例"""

        def run_one_case(case_info: dict | str):
            time.sleep(2)
            logger.info(case_info)
            return case_info

        def one_user_running():
            while True:
                if self.task.context.done():
                    return None
                case = get_case(self.task.job_instance_id)
                if case is None:
                    return None
                run_one_case(case)
                reset_count = get_cases_count(self.task.job_instance_id)
                progress = f"{self.cases_count - reset_count}/{self.cases_count}"
                self.task.update_progress(progress)
                progress_percent = int((self.cases_count - reset_count) * 100 / self.cases_count)
                self.task.update_progress_percent(progress_percent)

        users = []
        for i in range(5):
            u = threading.Thread(target=one_user_running)
            u.daemon = True
            u.start()
            users.append(u)

        [u.join() for u in users]
        logger.info("success")

    def success(self, *args, **kwargs):
        ...


__all__ = (
    'NLPUser',
)
