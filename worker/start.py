# -*- coding:utf-8 -*-
from worker.runner import TaskListenThread

task_thread = TaskListenThread()

task_thread.daemon = True

task_thread.start()

task_thread.join()
