from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'priority', 'status', 
            'due_date', 'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()

    def validate_due_date(self, value):
        if value:
            from django.utils import timezone
            if value < timezone.now():
                raise serializers.ValidationError("Due date cannot be in the past.")
        return value


class TaskCreateSerializer(TaskSerializer):
    class Meta(TaskSerializer.Meta):
        fields = [
            'title', 'description', 'priority', 'status', 'due_date'
        ]


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'priority', 'status', 'due_date'
        ]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()
