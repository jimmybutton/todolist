from django.urls import path

from .views import TodolistView, TodoDeleteView,  TodoToggleView

urlpatterns = [
    path('', TodolistView.as_view(), name='todo_list'),
    path('<int:pk>/delete/', TodoDeleteView.as_view(), name='todo_delete'),
    path('<int:pk>/toggle/', TodoToggleView.as_view(), name='todo_toggle'),
]