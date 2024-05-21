# -*- coding:utf-8 -*-
from rest_framework import viewsets

from apps.system.permission import RbacPermission


class CommonAViewSet(viewsets.ModelViewSet):
    permission_classes = [RbacPermission]
    ordering = ['-create_time']

    def perform_create(self, serializer):
        serializer.save(create_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(update_by=self.request.user)

    def perform_destroy(self, instance):
        instance.update_by = self.request.user
        instance.delete()
