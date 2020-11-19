from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from apiv1.models import Task, User
from apiv1.serializers import TaskSerializer, UserSerializer
from apiv1.permissions import IsLoggedInUserOrAdmin, IsAdminUser

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif (self.action == 'retrieve'
              or self.action == 'update'
              or self.action == 'partial_update'):
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
