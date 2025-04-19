from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_tournaments, name='list_tournaments'),
    path('create/', views.create_tournament, name='create_tournament'),
]
