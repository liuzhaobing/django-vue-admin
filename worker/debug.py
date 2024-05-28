# -*- coding:utf-8 -*-


def run():
    from worker.manager import TaskManager, TaskInfo, TaskPlan
    from worker.runner import TaskThread

    plan: TaskPlan = TaskPlan(type_name="nlp")
    task: TaskInfo = TaskInfo(type_name="nlp", type="1")
    plan.type_name_en = task.type_name_en
    plan.type_name = task.type_name

    new_task = TaskManager(name=task.name, type=task.type, type_name_en=task.type_name_en, type_name=task.type_name,
                           job_instance_id=task.job_instance_id)

    TaskThread(new_task, plan).start()


if __name__ == '__main__':
    run()
