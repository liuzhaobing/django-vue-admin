# -*- coding:utf-8 -*-
import os
import copy
import base64
import logging
import datetime
import threading
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass

from utils import context as _context
from worker.tasks import (update_task, status_change, broadcast_finished_task, close_cases,
                          STATUS, update_task_info, delete_task_info)

logger = logging.getLogger("log")
TASKS = {}
task_lock = threading.Lock()


@dataclass
class TaskStatus:
    QUEUEING: str = "1024"
    PREPARE: str = "512"
    RUNNING: str = "256"
    STOPPED: str = "128"
    FAILURE: str = "64"
    SUCCESS: str = "32"


@dataclass
class TaskMessage:
    QUEUEING: str = "任务排队中!"
    PREPARE: str = "任务准备中!"
    RUNNING: str = "任务执行中!"
    STOPPED: str = "任务停止成功!"
    FAILURE: str = "任务执行失败!"
    SUCCESS: str = "任务执行成功!"


class BaseClass:
    def __init__(self, **kwargs: Any):
        for key, value in kwargs.items():
            setattr(self, key, value)


class TaskInfo(BaseClass):
    def __init__(self, **kwargs: Any):
        self.name: str = ""
        self.job_instance_id: str = ""
        self.plan_id: str = ""
        self.type: str = ""
        self.type_name: str = ""
        self.type_name_en: str = ""
        self.status: str = TaskStatus.QUEUEING
        self.status_name: str = "队列中"
        self.progress: str = "0/0"
        self.progress_percent: str = "0"
        self.metrics: str = ""
        self.message: str = ""
        self.case_file: str = ""
        self.result_file: str = ""
        self.start_time: str = ""
        self.end_time: str = ""
        self.context: Optional[_context.Context] = None
        self.pass_count = 0
        self.fail_count = 0
        self.total_count = 0
        super().__init__(**kwargs)


class TaskPlan(BaseClass):
    def __init__(self, **kwargs: Any):
        self.id: str = ""
        self.name: str = ""
        self.config: str = ""
        self.data_source: str = ""
        self.type: str = ""
        self.type_name: str = ""
        self.type_name_en: str = ""
        super().__init__(**kwargs)


class TaskManager(TaskInfo):
    """任务状态控制器"""

    @property
    def info(self):
        """获取任务信息"""
        _info = copy.deepcopy(self.__dict__)
        del _info["context"]
        return _info

    def generate_job_instance_id(self):
        """生成任务实例ID"""
        now = datetime.datetime.now()
        _id = self.type_name_en.upper() + now.strftime("%Y%m%d%H%M%S") + base64.b32encode(os.urandom(5)).decode("ascii")
        if not self.job_instance_id:
            self.job_instance_id = _id
        return self.job_instance_id

    def prepare(self, message: str = TaskMessage.PREPARE):
        logger.info(f"task prepare start with task_name: {self.name}")
        self.status = TaskStatus.PREPARE
        self.status_name = "准备中"
        self.message = message

        now = datetime.datetime.now()
        self.start_time = now.strftime("%Y-%m-%d %H:%M:%S")

        _id = self.type_name_en.upper() + now.strftime("%Y%m%d%H%M%S") + base64.b32encode(os.urandom(5)).decode("ascii")
        if not self.job_instance_id:
            self.job_instance_id = _id
        self.context = _context.Context()
        with task_lock:
            TASKS[self.job_instance_id] = self
            update_task(self.job_instance_id, self.info)

    def running(self, message: str = TaskMessage.RUNNING):
        """任务执行中发送运行信号"""
        with task_lock:
            task = TASKS.get(self.job_instance_id)
            if task:
                task.status = TaskStatus.RUNNING
                task.status_name = "执行中"
                task.message = message
                update_task(self.job_instance_id, self.info)
                logger.info(f"task running start with job_instance_id: {self.job_instance_id}")
                return
            logger.error(f"task running start failed reason: invalid job_instance_id {self.job_instance_id}")
            return

    def success(self, result_file: str, message: str = TaskMessage.SUCCESS):
        """任务执行完成发送成功信号"""
        with task_lock:
            task = TASKS.get(self.job_instance_id)
            if task:
                task.result_file = result_file
                task.status = TaskStatus.SUCCESS
                task.message = message
                logger.info(f"task success job_instance_id: {self.job_instance_id}")
                logger.info(f"task success result_file: {task.result_file}")
                delete_task_info(self.job_instance_id)
                close_cases(self.job_instance_id)
                self.fire(status=TaskStatus.SUCCESS, message=message)
                return
            logger.error(f"task success start failed reason: invalid job_instance_id {self.job_instance_id}")
            return

    def stop(self, message: str = TaskMessage.STOPPED):
        """执行过程中用户主动停止"""
        with task_lock:
            task = TASKS.get(self.job_instance_id)
            if task:
                task.status = TaskStatus.STOPPED
                task.message = message
                logger.info(f"task stop with job_instance_id: {self.job_instance_id}")
                self.fire(status=TaskStatus.STOPPED, message=message)
                return
            logger.error(f"task stop start failed reason: invalid job_instance_id {self.job_instance_id}")
            return

    def failure(self, message: str = TaskMessage.FAILURE):
        """执行过程中遇到error 取消任务执行"""
        with task_lock:
            task = TASKS.get(self.job_instance_id)
            if task:
                task.status = TaskStatus.FAILURE
                task.message = message
                logger.info(f"task failure job_instance_id: {self.job_instance_id}")
                self.fire(status=TaskStatus.FAILURE, message=message)
                return
            logger.error(f"task failure start failed reason: invalid job_instance_id {self.job_instance_id}")
            return

    def fire(self, status, message):
        """任务结束 销毁内存任务 记录到数据库"""
        task = TASKS.get(self.job_instance_id)
        if task:
            task.status = status
            task.message = message
            task.context.cancel()
            task.end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            task_info = copy.deepcopy(task)
            del task_info.context

            update_task_info(self.job_instance_id, self.info)
            if task.status in [STATUS.STOPPED, TaskStatus.STOPPED]:
                status_change(self.job_instance_id, STATUS.RUNNING, STATUS.STOPPED)
            else:
                status_change(self.job_instance_id, STATUS.RUNNING, STATUS.FINISHED)
            broadcast_finished_task(self.job_instance_id, status)
            del TASKS[self.job_instance_id]

            return task_info.__dict__
        logger.error(f"task fire start failed reason: invalid job_instance_id {self.job_instance_id}")
        return

    def update_progress(self, progress: str):
        """更新任务进度"""
        with task_lock:
            task = TASKS.get(self.job_instance_id)
            if task:
                task.progress = progress
                update_task(self.job_instance_id, self.info)
                return
            logger.error(f"task update progress failed reason: invalid job_instance_id {self.job_instance_id}")
            return

    def update_accuracy(self, accuracy: float):
        """更新任务准确率"""
        with task_lock:
            task = TASKS.get(self.job_instance_id)
            if task:
                task.metrics = round(accuracy, 5)
                update_task(self.job_instance_id, self.info)
                return
            logger.error(f"task update accuracy failed reason: invalid job_instance_id {self.job_instance_id}")
            return

    def update_progress_percent(self, progress_percent: int):
        """更新用例进度百分比"""
        with task_lock:
            task = TASKS.get(self.job_instance_id)
            if task:
                task.progress_percent = progress_percent
                update_task(self.job_instance_id, self.info)
                return
            logger.error(f"task update progress_percent failed reason: invalid job_instance_id {self.job_instance_id}")
            return

    def update_message(self, message: str):
        """更新任务信息"""
        with task_lock:
            task = TASKS.get(self.job_instance_id)
            if task:
                task.message = message
                update_task(self.job_instance_id, self.info)
                return
            logger.error(f"task update message failed reason: invalid job_instance_id {self.job_instance_id}")
            return

    def update_status(self, status: int):
        """更新任务状态码"""
        with task_lock:
            task = TASKS.get(self.job_instance_id)
            if task:
                task.status = status
                update_task(self.job_instance_id, self.info)
                return
            logger.error(f"task update status failed reason: invalid job_instance_id {self.job_instance_id}")
            return


def get_running_task_list():
    """获取正在运行的任务列表"""
    running_task_list = []
    with task_lock:
        tasks = copy.deepcopy(TASKS)
        logger.info(f"find running TASKS: {TASKS}")

    if tasks:
        for _, task in tasks.items():
            del task.context
            running_task_list.append(task.__dict__)
    return running_task_list


Task = str


class Progress:
    def __init__(self, file: str) -> None:
        self.file = Path(file)
        self.completed: list[Task] = []

    def load(self) -> bool:
        if not self.file.exists():
            return False
        with threading.Lock():
            with self.file.open() as f:
                for line in f:
                    self.completed.append(line.strip())
        return len(self.completed) > 0

    def add(self, item: Task) -> None:
        self.completed.append(item)
        self.save()

    def save(self) -> None:
        self.file.parent.mkdir(parents=True, exist_ok=True)
        with threading.Lock():
            with self.file.open("w") as f:
                for item in self.completed:
                    f.write(item + "\n")
                logger.info(f"Saved progress to {self.file}")
