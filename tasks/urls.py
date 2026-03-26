from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_task, name='create_task'),
    path('', views.list_tasks, name='list_tasks'),
    path('<int:task_id>/', views.get_task, name='get_task'),
    path('<int:task_id>/update/', views.update_task, name='update_task'),
    path('<int:task_id>/delete/', views.delete_task, name='delete_task'),
]
