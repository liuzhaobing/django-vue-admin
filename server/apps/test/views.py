# -*- coding:utf-8 -*-
import json
from datetime import datetime
import bson

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from server import mongo_db, settings
from utils.tools import generate_trace_id
from utils.view import CommonAViewSet
from .filter import PlanFilter, TaskFilter
from .models import (
    Status,
    Type,
    Group,
    Plan,
    Task,
    Report,
    Log,
)
from .serializers import (
    StatusSerializer,
    TypeSerializer,
    GroupSerializer,
    PlanSerializer,
    TaskSerializer,
    ReportSerializer,
    LogSerializer,
)
from .tasks import *
from .tasks import update_task_info, get_tasks
from ..system.models import File
from ..system.permission import RbacPermission
from ..system.serializers import FileSerializer


class FileViewSet(CreateModelMixin, GenericViewSet):
    """
    文件上传用
    """
    perms_map = {}
    permission_classes = []
    parser_classes = [MultiPartParser, JSONParser]
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filterset_fields = ['type']
    search_fields = ['name']
    ordering = ['-create_time']

    def perform_create(self, serializer):
        file_obj = self.request.data.get('file')
        name = file_obj._name
        size = file_obj.size
        mime = file_obj.content_type
        tp = '其它'
        if 'image' in mime:
            tp = '图片'
        elif 'video' in mime:
            tp = '视频'
        elif 'audio' in mime:
            tp = '音频'
        elif 'application' or 'text' in mime:
            tp = '文档'
        instance = serializer.save(create_by=self.request.user, name=name, size=size, type=tp, mime=mime)
        instance.path = settings.MEDIA_URL + instance.file.name
        instance.save()


class StatusViewSet(CommonAViewSet):
    perms_map = {'get': '*', 'post': 'status_create',
                 'put': 'status_update', 'delete': 'status_delete'}
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class TypeViewSet(CommonAViewSet):
    perms_map = {'get': '*', 'post': 'type_create',
                 'put': 'type_update', 'delete': 'type_delete'}
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class GroupViewSet(CommonAViewSet):
    perms_map = {'get': '*', 'post': 'group_create',
                 'put': 'group_update', 'delete': 'group_delete'}
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PlanViewSet(CommonAViewSet):
    perms_map = {'get': '*', 'post': 'plan_create',
                 'put': 'plan_update', 'delete': 'plan_delete'}
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    filterset_class = PlanFilter

    @action(methods=['get'], detail=True, permission_classes=[RbacPermission], perms_map={'post': 'task_publish'},
            url_name='publish')
    def _publish(self, request, pk: int = None):
        """任务发布"""
        # 0.find out the plan information
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        plan = serializer.data
        # 1.publish plan information to redis
        update_plan(pk, dict(plan))
        # 2.publish task information to redis
        task = {
            "name": instance.name,
            "job_instance_id": generate_trace_id(instance.type.name_en),
            "plan_id": pk,
            "type": instance.type.id,
            "type_name": instance.type.name,
            "type_name_en": instance.type.name_en,
            "status": 1024,
            "status_name": "队列中",
            "progress": "0/0",
            "progress_percent": 0,
            "create_by": request.user.id,
            "create_user": request.user.name,
        }
        update_task(task['job_instance_id'], task)
        # 3.redis change status
        status_change(task['job_instance_id'], STATUS.STOPPED, STATUS.RUNNING)
        # 4.publish sequence to task channel
        sequence = {"plan_id": pk, "job_instance_id": task['job_instance_id'], "execute_type": "start"}
        publish_task(task['type_name_en'], json.dumps(sequence, ensure_ascii=False))
        return Response(plan, status=status.HTTP_201_CREATED)


class TaskViewSet(CommonAViewSet):
    perms_map = {'get': '*', 'post': 'task_create',
                 'put': 'task_update', 'delete': 'task_delete'}
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter

    @action(methods=['get'], detail=False, permission_classes=[RbacPermission], perms_map={'get': 'task_running'},
            url_name='running')
    def _running(self, request):
        """查询运行中的任务"""
        tasks = list_tasks(dict(request.query_params), STATUS.RUNNING)
        response_data = {
            'count': len(tasks),
            'previous': None,
            'next': None,
            'results': tasks
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=True, permission_classes=[RbacPermission], perms_map={'get': 'task_deletion'},
            url_name='deletion')
    def _deletion(self, request, pk: str = None):
        """删除僵尸任务"""
        tasks = get_tasks()
        if pk in tasks:
            last_active_time_string = tasks[pk]
            if datetime.now().timestamp() - float(last_active_time_string) > 300:
                delete_task_info(pk)
                close_cases(pk)
                return Response(destroy_task(pk), status=status.HTTP_204_NO_CONTENT)
            return Response(data={'msg': '任务最近5分钟内有活跃，请稍后再试！'})
        return Response(data={'msg': '任务不存在！'})

    @action(methods=['post'], detail=True, permission_classes=[RbacPermission], perms_map={'post': 'task_stop'},
            url_name='stop')
    def _stop(self, request, pk: str = None):
        """停止任务"""
        # 0.find out the task information
        task = retrieve_task(pk)
        # 1.redis change status
        update_task_info(task['job_instance_id'], {'update_by': request.user.id})
        # 2.notify worker to stop
        sequence = {"job_instance_id": task['job_instance_id'], "execute_type": "stop"}
        publish_task(task['type_name_en'], json.dumps(sequence, ensure_ascii=False))
        return Response(task, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, permission_classes=[RbacPermission], perms_map={'post': 'task_continue'},
            url_name='continue')
    def _continue(self, request, pk: int = None):
        """任务断点续传"""
        # 0.find out the task information
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        task = serializer.data
        task_info = self._retrieve_task(task['job_instance_id'])
        # 1.redis change status
        status_change(task_info['job_instance_id'], STATUS.STOPPED, STATUS.RUNNING)
        # 2.notify worker to continue
        sequence = {"job_instance_id": task_info['job_instance_id'], "execute_type": "continue"}
        publish_task(task_info['type_name'], json.dumps(sequence, ensure_ascii=False))
        # 3.task record remove from mysql table
        self.perform_destroy(instance)
        return Response(task_info)


class LogViewSet(CommonAViewSet):
    permission_classes = [RbacPermission]
    queryset = Log.objects.all()
    serializer_class = LogSerializer

    @action(methods=['post'], detail=True, permission_classes=[RbacPermission], perms_map={'post': 'log_list'},
            url_name='log')
    def _list(self, request, task_type='0', *args, **kwargs):
        """request.data is a mongo aggregate pipline like"""
        collection = mongo_db[task_type]
        results_count = collection.count_documents(request.data[0].get('$match', {}))
        results_cursor = collection.aggregate_raw_batches(request.data)
        results_data = [bson.decode_all(row) for row in results_cursor]
        response_data = {
            'count': results_count,
            'previous': None,
            'next': None,
            'results': results_data[0] if results_data else None
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=True, permission_classes=[RbacPermission], perms_map={'put': 'log_update'},
            url_name='log')
    def _update(self, request, task_type='0', *args, **kwargs):
        collection = mongo_db[task_type]
        return Response(data={}, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=True, permission_classes=[RbacPermission], perms_map={'delete': 'log_delete'},
            url_name='log')
    def _destroy(self, request, task_type='0', *args, **kwargs):
        collection = mongo_db[task_type]
        return Response(data={}, status=status.HTTP_200_OK)


class ReportViewSet(CommonAViewSet):
    perms_map = {'get': '*', 'post': 'report_create',
                 'put': 'report_update', 'delete': 'report_delete'}
    permission_classes = [RbacPermission]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
