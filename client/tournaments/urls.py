from django.urls import path
from .views import *

urlpatterns = [
    path("create/", CreateTournament.as_view(), name="create_tournament"),
    path("<int:id>/start/", StartTournament.as_view(), name="start_tournament"),
    #path("<int:id>/"),
    #path("<int:id>/rounds/"),
    #path("<int:id>/current-round/"),
]
