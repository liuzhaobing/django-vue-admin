# -*- coding:utf-8 -*-
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

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
from ..system.permission import RbacPermission


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


class TaskViewSet(CommonAViewSet):
    perms_map = {'get': '*', 'post': 'task_create',
                 'put': 'task_update', 'delete': 'task_delete'}
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter

    @action(methods=['get'], detail=False, permission_classes=[RbacPermission], perms_map={'post': 'task_running'},
            url_name='running')
    def _running(self, request):
        """查询运行中的任务"""
        return Response(data=[], status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permission_classes=[RbacPermission], perms_map={'post': 'task_stop'},
            url_name='stop')
    def _stop(self, request, pk=None):
        """停止任务"""
        return Response(data={}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permission_classes=[RbacPermission], perms_map={'post': 'task_continue'},
            url_name='continue')
    def _continue(self, request, pk=None):
        """任务断点续传"""
        return Response(data={}, status=status.HTTP_200_OK)


class LogViewSet(CommonAViewSet):
    perms_map = {'get': '*', 'post': 'log_create',
                 'put': 'log_update', 'delete': 'log_delete'}
    permission_classes = [RbacPermission]
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class ReportViewSet(CommonAViewSet):
    perms_map = {'get': '*', 'post': 'report_create',
                 'put': 'report_update', 'delete': 'report_delete'}
    permission_classes = [RbacPermission]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
