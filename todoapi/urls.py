from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('completedtodo/', views.ListCompleted.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('todos/', views.TodoListCreate.as_view()),
    path('todos/<int:pk>', views.TodoRetrieveUpdateDestroy.as_view()),
    path('todos/<int:pk>/complete', views.TodoComplete.as_view()), 
    path('signup/', views.signup),
    path('login/', views.login),
]