from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.task_create, name='task_create'),
    path('delete/<int:pk>/', views.soft_delete, name='soft_delete'),
    path('trash/', views.trash_bin, name='trash_bin'),
    path('restore/<int:task_id>/', views.restore_task, name='restore_task'),
    path('delete-forever/<int:task_id>/', views.delete_forever, name='delete_forever'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
    path('tasks/', views.task_list, name='task_list'),
]