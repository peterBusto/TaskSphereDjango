from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer
from .models import Task


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_task(request):
    """
    Create a new task for the authenticated user.
    """
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        task = serializer.save(user=request.user)
        response_serializer = TaskSerializer(task)
        return Response({
            'message': 'Task created successfully',
            'task': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_tasks(request):
    """
    Get all tasks for the authenticated user
    """
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response({
        'tasks': serializer.data,
        'count': tasks.count()
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_task(request, task_id):
    """
    Get a specific task by ID
    """
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_task(request, task_id):
    """
    Update a specific task
    """
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            updated_task = serializer.save()
            response_serializer = TaskSerializer(updated_task)
            return Response({
                'message': 'Task updated successfully',
                'task': response_serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_task(request, task_id):
    """
    Delete a specific task
    """
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        task.delete()
        return Response({'message': 'Task deleted successfully'}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
