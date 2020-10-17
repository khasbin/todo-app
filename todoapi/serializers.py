from rest_framework import serializers
from todo.models import Todoapp

class TodoListSerializer(serializers.ModelSerializer):
    created_date = serializers.ReadOnlyField()
    date_completed = serializers.ReadOnlyField()
    class Meta:
         model = Todoapp
         fields = ['id','name', 'memo','created_date','date_completed', 'important']


class TodoCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todoapp
        fields = ['id']
        read_only_fields = ['name', 'memo','created_date','date_completed', 'important']