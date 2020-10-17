from django.shortcuts import render
from rest_framework import generics, mixins
from .serializers import TodoListSerializer, TodoCompleteSerializer
from todo.models import Todoapp
from rest_framework import permissions
from django.utils import timezone

# Create your views here.

class ListCompleted(generics.ListAPIView):
    serializer_class = TodoListSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Todoapp.objects.filter(user = self.request.user, date_completed__isnull = False).order_by("-date_completed")


class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoListSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Todoapp.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todoapp.objects.filter(user = user)


class TodoComplete(generics.UpdateAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todoapp.objects.filter(user = user)
    
    def perform_update(self, serializer):
        serializer.instance.date_completed = timezone.now()
        serializer.save()





    