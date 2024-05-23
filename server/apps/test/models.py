# -*- coding:utf-8 -*-
import json
import threading

from django.db import models
import django.utils.timezone as timezone

from .tasks import listening_finished_task, listening_task_report
from ..system.models import CommonAModel


class Status(CommonAModel):
    name = models.CharField('状态名称', max_length=32)

    class Meta:
        verbose_name = '状态'
        verbose_name_plural = verbose_name


class Type(CommonAModel):
    name = models.CharField('类型名称', max_length=64, unique=True)
    name_en = models.CharField('类型名称en', max_length=64, unique=True)
    description = models.TextField('类型描述', blank=True, null=True)
    status = models.ForeignKey(
        Status, verbose_name='类型状态', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = '任务类型'
        verbose_name_plural = verbose_name


class Group(CommonAModel):
    name = models.CharField('名称', max_length=64, unique=True)

    class Meta:
        verbose_name = '分组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Plan(CommonAModel):
    name = models.CharField('名称', max_length=64, unique=True)
    type = models.ForeignKey(
        Type, verbose_name='计划类型', on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group, verbose_name='分组', on_delete=models.CASCADE
    )
    config = models.TextField('计划参数配置')
    data_source = models.TextField('数据源')

    class Meta:
        verbose_name = '测试计划'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Task(CommonAModel):
    name = models.CharField('名称', max_length=64)
    job_instance_id = models.CharField('任务ID', max_length=128)
    plan_id = models.ForeignKey(
        Plan, verbose_name='计划ID', on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        Type, verbose_name='任务类型', on_delete=models.CASCADE
    )
    status = models.ForeignKey(
        Status, verbose_name='任务状态', on_delete=models.CASCADE
    )
    progress = models.CharField('执行进度', max_length=128, blank=True, null=True)
    progress_percent = models.IntegerField('进度百分比', default=0)
    metrics = models.TextField('评测指标', blank=True, null=True)
    message = models.TextField('任务消息', blank=True, null=True)
    case_file = models.CharField('测试用例文件', max_length=512, blank=True, null=True)
    result_file = models.CharField('测试结果文件', max_length=512, blank=True, null=True)
    start_time = models.DateTimeField(default=timezone.now, verbose_name='开始时间', help_text='开始时间')
    end_time = models.DateTimeField(default=timezone.now, verbose_name='结束时间', help_text='结束时间')

    class Meta:
        verbose_name = '测试任务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Log(CommonAModel):
    name = models.CharField('名称', max_length=64, unique=True)

    class Meta:
        verbose_name = '执行日志'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Report(CommonAModel):
    name = models.CharField('报告名称', max_length=64)
    job_instance_id = models.CharField('任务ID', max_length=128)
    data = models.TextField('测试报告数据', blank=True, null=True)

    class Meta:
        verbose_name = '测试报告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ReportListenThread(threading.Thread):
    def run(self):
        for message in listening_task_report():
            payload = json.loads(message)
            Report.objects.create(**payload)


class TaskListenThread(threading.Thread):
    def run(self):
        for message in listening_finished_task():
            payload = json.loads(message)
            Task.objects.create(**payload)


TaskListenThread().start()
ReportListenThread().start()
