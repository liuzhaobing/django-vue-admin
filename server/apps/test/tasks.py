# -*- coding:utf-8 -*-
import logging
import datetime
import dataclasses
import json

from utils.client import *

logger = logging.getLogger("log")


@dataclasses.dataclass
class STATUS:
    RUNNING = "RUNNING_JOBS"
    STOPPED = "STOPPED_JOBS"
    FINISHED = "FINISHED_JOBS"


def delete_task(job_instance_id: str, tp: str = STATUS.RUNNING):
    logger.info(f"delete task: {job_instance_id}")
    return hash_delete_key(tp, job_instance_id)


def get_tasks(tp: str = STATUS.RUNNING) -> dict | None:
    logger.info(f"get tasks: {tp}")
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
    logger.info(f"get task config: {job_instance_id}")
    return hash_get_all(f"{job_instance_id}")


def delete_task_info(job_instance_id: str):
    logger.info(f"delete task config: {job_instance_id}")
    return hash_delete_table(f"{job_instance_id}")


def update_plan_info(plan_id: str | int, data: dict | None):
    logger.info(f"update plan config: {plan_id}")
    if not data:
        return False
    for key, value in data.items():
        hash_set(f"PLAN_{plan_id}", key, value if not isinstance(value, bool) else str(value))
    return True


def get_plan_info(plan_id: str | int):
    logger.info(f"get plan config: {plan_id}")
    return hash_get_all(f"PLAN_{plan_id}")


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
    logger.info(f"list tasks: {tp}")
    return _tasks


def retrieve_task(job_instance_id: str) -> dict | None:
    """获取单个任务详情"""
    task = get_task_info(job_instance_id)
    for key in [
        "plan_id",
        "create_by",
        "update_by",
        "type",
        "status",
        "progress_percent",
    ]:
        if key in task:
            task[key] = int(task[key])
    logger.info(f"retrieve task config: {job_instance_id}")
    return task


def destroy_task(job_instance_id: str, tp: str = STATUS.RUNNING) -> dict:
    """从单个状态中删除任务"""
    logger.info(f"destroy task: {job_instance_id} from: {tp}")
    return delete_task(job_instance_id, tp)


def status_change(job_instance_id: str, old_status, new_status):
    """任务状态变更"""
    logger.info(f"status change: {job_instance_id} from: {old_status} to: {new_status}")
    destroy_task(job_instance_id, old_status)
    update_task_last_active_time(job_instance_id, new_status)
    return True


def update_plan(plan_id: str | int, data: dict | None) -> bool:
    """更新计划信息"""
    logger.info(f"update plan config: {plan_id}")
    return update_plan_info(plan_id, data)


def retrieve_plan(plan_id: str | int) -> bool:
    """获取计划信息"""
    logger.info(f"retrieve plan config: {plan_id}")
    return get_plan_info(plan_id)


def publish_task(task_type_name_en: str, msg: str):
    """发布测试任务到消息队列"""
    logger.info(f"publish task to channel: {task_type_name_en}")
    return push_to_queue(f"TASK_{task_type_name_en}", msg)


def claim_task(task_type_name_en: str):
    """从消息队列领取测试任务"""
    logger.info(f"claim task: {task_type_name_en}")
    return subscribe_queue(f"TASK_{task_type_name_en}")


def inspect_task_channel(task_type_name_en: str):
    """查阅消息队列中的测试任务"""
    logger.info(f"inspect task channel: {task_type_name_en}")
    return get_queue_elements(f"TASK_{task_type_name_en}")


def listening_finished_task():
    """监听worker已执行完成的任务"""
    logger.info(f"listening finished task channel: STATUS_FINISHED")
    return subscribe_queue("STATUS_FINISHED")


def listening_task_report():
    """监听worker发表的测试报告"""
    logger.info(f"listening task report channel: TASK_REPORT")
    return subscribe_queue("TASK_REPORT")


def broadcast_finished_task(job_instance_id: str, status: str | int):
    logger.info(f"push finished task channel: {job_instance_id} {status}")
    return push_to_queue("STATUS_FINISHED",
                         json.dumps({"job_instance_id": job_instance_id, "status": status}, ensure_ascii=False))


def broadcast_task_report(data: str | dict):
    logger.info(f"push task report to channel: TASK_REPORT")
    return push_to_queue("TASK_REPORT", json.dumps(data, ensure_ascii=False) if isinstance(data, dict) else data)


def publish_case(job_instance_id: str, msg):
    """发布测试用例到消息队列"""
    return push_to_queue(f"CASE_{job_instance_id}", msg)


def get_case(job_instance_id: str):
    """从消息队列领取测试用例"""
    return pop_from_queue(f"CASE_{job_instance_id}")


def inspect_cases(job_instance_id: str):
    """查阅消息队列中的测试用例"""
    return get_queue_elements(f"CASE_{job_instance_id}")


def get_cases_count(job_instance_id: str):
    return get_queue_elements_count(f"CASE_{job_instance_id}")


def close_cases(job_instance_id: str):
    """关闭用例队列"""
    logger.info(f"close cases channel: {job_instance_id}")
    return close_queue(f"CASE_{job_instance_id}")


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
    "broadcast_finished_task",
    "broadcast_task_report",

    "get_plan_info",
    "get_task_info",

    "get_case",
    "close_cases",
    "publish_case",
    "inspect_cases",
    "get_cases_count",

    "delete_task_info",
    "update_task_info",
)
