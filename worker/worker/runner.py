# -*- coding:utf-8 -*-
import json
import logging
import threading
import concurrent.futures
from typing import Callable
from multiprocessing.pool import ThreadPool

from .model import TaskModel
from utils import context as _context
from .manager import TaskManager, TaskPlan, TaskInfo, TASKS
from .tasks import claim_task, get_plan_info, get_task_info
from .worker import *

logger = logging.getLogger("log")


class TaskRunner:
    """任务调度控制"""

    def __init__(self,
                 task: TaskManager,
                 ctx: _context.Context,
                 function: Callable,
                 work_items: list,
                 threads: int):
        self.task = task
        self.ctx = ctx
        self.function = function
        self.finished_items = []
        self.work_items = work_items
        self.threads = threads
        self.pass_count, self.fail_count = 0, 0

    def __call__(self):
        with ThreadPool(self.threads) as pool:
            iter = pool.imap_unordered(self._worker_thread_with_context, self.work_items)
            for item in iter:
                self.finished_items.append(item)
                self._update_progress(item)
        return self.finished_items

    def _worker_thread_with_context(self, *args, **kwargs):
        result = {}
        if self.ctx.done():
            return result

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        future = executor.submit(self.function, *args, **kwargs)
        try:
            result = future.result(timeout=300)
        except concurrent.futures.TimeoutError as e:
            logger.info(f"concurrent.futures.TimeoutError with function [{self.function}] input [{args}][{kwargs}]")
            future.cancel()
        finally:
            executor.shutdown(wait=False)
            return result

    @property
    def _work_items_count(self):
        return len(self.work_items)

    @property
    def _finished_items_count(self):
        return len(self.finished_items)

    def _update_progress(self, item):
        index, count = self._finished_items_count, self._work_items_count
        self.task.progress_percent = int(100 * index / count)
        self.task.progress = f"{index}/{count}"
        if item.__contains__("pass"):
            if item["pass"]:
                self.pass_count += 1
            else:
                self.fail_count += 1
            self.task.accuracy = self.pass_count / (self.pass_count + self.fail_count)
        return self.task.progress_percent


class TaskThread(threading.Thread):
    def __init__(self, task: TaskManager, plan: TaskPlan):
        logger.info(f"new a TaskThread success for task_name: {plan.name}")
        threading.Thread.__init__(self)
        _task_model = InitTaskModel(plan=plan, task=task)
        self.job = BaseTask(_task_model, task)

    def run(self):
        self.job.run()


class BaseTask:
    def __init__(self, model: TaskModel, task: TaskManager):
        self.task_model = model
        self.task = task

    def run(self):
        self.task_model.prepare()
        self.task.prepare()

        self.task.running()
        self.task_model.run()

        self.task_model.end()


def InitTaskModel(task: TaskManager, plan: TaskPlan) -> TaskModel:
    for model in TaskModel.__subclasses__():
        if model.TASK_TYPE == plan.type_name_en:
            logger.info(f"init task model success! [{plan.type_name_en}]")
            return model(task, plan)
    logger.error(f"init task model failed reason: not find task_type! [{plan.type_name_en}]")


class TaskListenThread(threading.Thread):

    @property
    def models(self):
        return [model.TASK_TYPE for model in TaskModel.__subclasses__()]

    def run(self):
        for task_q in claim_task(*self.models):  # 申领任务
            task_q_json = json.loads(task_q)
            execute_type = task_q_json["execute_type"]
            """
            task_q_json = {"plan_id": "", "job_instance_id": "", "execute_type": ""}
            """
            if execute_type == "stop":
                with threading.Lock():
                    task = TASKS.get(task_q_json["job_instance_id"])
                    if task:
                        task.stop()
            else:
                plan_info = get_plan_info(task_q_json["plan_id"])  # 获取计划信息
                task_info = get_task_info(task_q_json["job_instance_id"])  # 获取任务信息
                plan: TaskPlan = TaskPlan(**plan_info)
                task: TaskManager = TaskManager(**task_info)
                plan.type_name = task.type_name
                plan.type_name_en = task.type_name_en
                thead = TaskThread(task, plan)
                thead.daemon = True
                thead.start()
