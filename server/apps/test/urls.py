# -*- coding:utf-8 -*-
from django.urls import include, path
from rest_framework import routers
from .views import (
    StatusViewSet,
    TypeViewSet,
    PlanViewSet,
    TaskViewSet,
    ReportViewSet,
    GroupViewSet,
    LogViewSet,
)

router = routers.DefaultRouter()
router.register(r'status', StatusViewSet)
router.register(r'type', TypeViewSet)
router.register(r'plan', PlanViewSet)
router.register(r'task', TaskViewSet)
router.register(r'report', ReportViewSet)
router.register(r'group', GroupViewSet)
router.register(r'log', LogViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
