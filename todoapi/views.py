from django.shortcuts import render
from rest_framework import generics, mixins
from .serializers import TodoListSerializer, TodoCompleteSerializer
from todo.models import Todoapp
from rest_framework.exceptions import ValidationError, status
from rest_framework import permissions
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Create your views here.
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(username = data['username'], password = data['password'])
            user.save()
            token = Token.objects.create(user = user)
            return JsonResponse({'token': str(token)}, status = 201)
        except IntegrityError:
            return JsonResponse({'error':"The username is already taken please choose another username"}, status = 400)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data =JSONParser().parse(request)
        user = User.objects.authenticate(username = data['username'], password= data['password'])
        if user is None:
            return JsonResponse({'error':'Could not login! please check your username and password'})
        else:
            try:
                token = Token.objects.get(user = user)
            except:
                token = Token.objects.create(user = user)
            return JsonResponse({'token': str(token)}, status = 201)

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





    