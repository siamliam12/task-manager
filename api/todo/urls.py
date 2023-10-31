from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('todo/', views.add_todo, name='add-todo'),
    path('alltodo/', views.view_todo, name='view-todo'),
    path('update/<int:pk>', views.update_todo, name='update-todo'),
    path('delete/<int:pk>', views.delete_todo, name='delete-todo'),
]