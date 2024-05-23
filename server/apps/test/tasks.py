# -*- coding:utf-8 -*-
import datetime
import dataclasses

from utils.client import *


@dataclasses.dataclass
class STATUS:
    RUNNING = "running_job_instance_id"
    STOPPED = "stopped_job_instance_id"
    FINISHED = "finished_job_instance_id"


def delete_task(job_instance_id: str, tp: str = STATUS.RUNNING):
    return hash_delete_key(tp, job_instance_id)


def get_tasks(tp: str = STATUS.RUNNING) -> dict | None:
    return hash_get_all(tp)


def update_task_last_active_time(job_instance_id: str, tp: str = STATUS.RUNNING,
                                 now_time: float = datetime.datetime.now().timestamp()):
    return hash_set(tp, job_instance_id, now_time)


def update_task_info(job_instance_id: str, data: dict | None, tp: str = STATUS.RUNNING) -> bool:
    if not data:
        return False
    for key, value in data.items():
        hash_set(job_instance_id, key, value)
    update_task_last_active_time(job_instance_id, tp)
    return True


def get_task_info(job_instance_id: str) -> dict | None:
    return hash_get_all(job_instance_id)


def delete_task_info(job_instance_id: str):
    return hash_delete_table(job_instance_id)


def update_plan_info(plan_id: str | int, data: dict | None):
    if not data:
        return False
    for key, value in data.items():
        hash_set(f"plan_{plan_id}", key, value if not isinstance(value, bool) else str(value))
    return True


def get_plan_info(plan_id: str | int):
    return hash_get_all(f"plan_{plan_id}")


"""the following are for outer interface"""


def update_task(job_instance_id: str, data: dict | None) -> bool:
    """刷新任务进度"""
    return update_task_info(job_instance_id, data)


def list_tasks(_filter: dict | None = None, tp: str = STATUS.RUNNING) -> list:
    """获取任务列表"""
    tasks = get_tasks(tp)
    if not tasks:
        return []
    _tasks = []
    for job_instance_id in tasks.keys():
        _task = retrieve_task(job_instance_id)
        if _task:
            if _filter:
                filter_keys = [key for key in _filter.keys() if key in _task and _filter[key]]
                if all(any(v in _task[key] for v in _filter[key]) for key in filter_keys):
                    _tasks.append(_task)
            else:
                _tasks.append(_task)
    return _tasks


def retrieve_task(job_instance_id: str) -> dict | None:
    """获取单个任务详情"""
    task = get_task_info(job_instance_id)
    task = {
        **task,
        "plan_id": int(task['plan_id']),
        "create_by": int(task['create_by']),
        "type": int(task['type']),
        "status": int(task['status']),
        "progress_percent": int(task['progress_percent']),
    }
    return task


def destroy_task(job_instance_id: str, tp: str = STATUS.RUNNING) -> dict:
    """从单个状态中删除任务"""
    return delete_task(job_instance_id, tp)


def status_change(job_instance_id: str, old_status, new_status):
    """任务状态变更"""
    destroy_task(job_instance_id, old_status)
    update_task_last_active_time(job_instance_id, new_status)
    return True


def update_plan(plan_id: str | int, data: dict | None) -> bool:
    """更新计划信息"""
    return update_plan_info(plan_id, data)


def retrieve_plan(plan_id: str | int) -> bool:
    """获取计划信息"""
    return get_plan_info(plan_id)


def publish_task(task_type_name_en: str, msg: str):
    """发布测试任务到消息队列"""
    return push_to_queue(f"task_{task_type_name_en}", msg)


def claim_task(task_type_name_en: str):
    """从消息队列领取测试任务"""
    return subscribe_channel(f"task_{task_type_name_en}")


def inspect_task_channel(task_type_name_en: str):
    """查阅消息队列中的测试任务"""
    return get_queue_elements(f"task_{task_type_name_en}")


def listening_finished_task():
    """监听worker已执行完成的任务"""
    return subscribe_channel(STATUS.FINISHED)


def listening_task_report():
    """监听worker发表的测试报告"""
    return subscribe_channel("task_report")


__all__ = (
    "STATUS",
    "update_task",
    "list_tasks",
    "retrieve_task",
    "destroy_task",
    "status_change",
    "update_plan",
    "retrieve_plan",
    "publish_task",
    "claim_task",
    "listening_finished_task",
    "listening_task_report",
)

if __name__ == '__main__':
    _job_instance_id: str = "SKILL20240507021000DYMKJ"
    _task_info = {
        "name": "大模型意图识别FIT环境-1819",
        "job_instance_id": _job_instance_id,
        "plan_id": 1,
        "type": 1,
        "status": 256,
        "progress": "56/100",
        "progress_percent": 56,
        "metrics": "[]",
        "message": "执行中！",
        "case_file": "/media/*.xlsx",
        "result_file": "/media/*.xlsx",
        "start_time": "2024-05-23 09:54:00",
        "end_time": "2024-05-23 09:59:00",
    }
    update_task(_job_instance_id, _task_info)
    print(list_tasks())
    # destroy_task(_job_instance_id)
    # print(list_tasks())
