from django.urls import path
from . import views

urlpatterns = [
    path('<int:battle_id>/manage/', views.manage_battle, name='manage_battle'),
    path('<int:battle_id>/add-event/', views.add_event, name='add_event'),
    path('<int:battle_id>/complete/', views.complete_battle, name='complete'),
    path('battles/pending/', views.pending_battles, name='pending_battles'),
]