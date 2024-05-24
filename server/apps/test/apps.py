import logging
from django.apps import AppConfig

logger = logging.getLogger("log")


class TestConfig(AppConfig):
    name = 'apps.test'
    verbose_name = '自动化测试'

    def ready(self):
        from .listener import TaskListenThread, ReportListenThread
        task_listener = TaskListenThread()
        task_listener.daemon = True
        task_listener.start()
        logger.info("任务监听线程启动~")

        report_listener = ReportListenThread()
        report_listener.daemon = True
        report_listener.start()
        logger.info("报告监听线程启动~")
