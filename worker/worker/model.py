# -*- coding:utf-8 -*-
import abc

from .manager import TaskManager


class TaskModel(abc.ABC):
    TASK_TYPE: str

    def __init__(self, task: TaskManager, plan):
        self.task = task
        self.plan = plan

    def __str__(self):
        return self.TASK_TYPE

    @abc.abstractmethod
    def prepare(self):
        raise NotImplementedError

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

    @abc.abstractmethod
    def end(self):
        raise NotImplementedError
