from django.urls import path
from . import views

urlpatterns = [ # urls dos torneios
    path('', views.list_tournaments, name='list_tournaments'),
    path('create/', views.create_tournament, name='create_tournament'),
    path('<int:tournament_id>/', views.tournament_detail, name='tournament_detail'), # Detalhes de um torneio específico, incluí as batalhas
]
