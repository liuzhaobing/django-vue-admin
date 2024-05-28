# -*- coding:utf-8 -*-
from rest_framework import serializers
from .models import (
    Status,
    Type,
    Group,
    Plan,
    Task,
    Report,
    Log,
)
from ..system.serializers import CommonASerializer


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PlanSerializer(CommonASerializer):
    type_name = serializers.CharField(source='type.name', read_only=True)
    type_name_en = serializers.CharField(source='type.name_en', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = Plan
        fields = (
            'id', 'name', 'config', 'data_source', 'type_name', 'type_name_en', 'group_name',
            'create_user', 'update_user', 'create_time', 'update_time', 'is_deleted',
        )


class TaskSerializer(CommonASerializer):
    type_name = serializers.CharField(source='type.name', read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)

    class Meta:
        model = Task
        fields = (
            'id', 'name', 'job_instance_id', 'plan_id', 'type_name', 'status', 'status_name',
            'progress', 'progress_percent', 'metrics', 'message',
            'case_file', 'result_file', 'start_time', 'end_time',
            'create_user', 'update_user', 'create_time', 'update_time', 'is_deleted',
        )


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'
