# -*- coding:utf-8 -*-
import json
import threading

from apps.system.models import User
from .models import Report, Plan, Type, Status, Task
from .tasks import listening_task_report, listening_finished_task, retrieve_task


class ReportListenThread(threading.Thread):
    def run(self):
        for message in listening_task_report():
            if message is None:
                continue
            payload = json.loads(message)
            Report.objects.create(**payload)


class TaskListenThread(threading.Thread):
    def run(self):
        for message in listening_finished_task():
            if message is None:
                continue
            payload = json.loads(message)
            job_instance_id = payload['job_instance_id']
            task_info = retrieve_task(job_instance_id)
            if 'plan_id' in task_info:
                if task_info['plan_id']:
                    task_info['plan_id'] = Plan.objects.get(pk=task_info['plan_id'])
            if 'create_by' in task_info:
                if task_info['create_by']:
                    task_info['create_by'] = User.objects.get(pk=task_info['create_by'])
            if 'update_by' in task_info:
                if task_info['update_by']:
                    task_info['update_by'] = User.objects.get(pk=task_info['update_by'])
            if 'type' in task_info:
                if task_info['type']:
                    task_info['type'] = Type.objects.get(pk=task_info['type'])
            if 'status' in task_info:
                if task_info['status']:
                    task_info['status'] = Status.objects.get(pk=task_info['status'])
            this_task_info = {}
            for k, v in task_info.items():
                if k in Task.__dict__.keys():
                    this_task_info[k] = v
            Task.objects.create(**this_task_info)
