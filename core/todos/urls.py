from django.urls import path
from . import views

urlpatterns = [
    path('', views.todos, name='todos'),
    path('<int:id>', views.todo, name='todo'),
]