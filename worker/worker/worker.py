# -*- coding:utf-8 -*-
from .model import TaskModel
from .user import *


class TaskNLP(TaskModel):
    TASK_TYPE = "nlp"

    def prepare(self):
        self.task = NLPUser(task=self.task, plan=self.plan)
        self.task.prepare()

    def run(self):
        self.task.start_running()

    def end(self):
        self.task.success()


__all__ = (
    'TaskNLP',
)
