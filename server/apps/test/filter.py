# -*- coding:utf-8 -*-
from django_filters import rest_framework as filters
from .models import Task, Plan


class PlanFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Plan
        fields = '__all__'


class TaskFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Task
        fields = '__all__'
