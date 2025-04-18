from django.urls import path
from .views import *

urlpatterns = [
    path("create/", CreateStartup.as_view(), name="create_startup"), #Cria uma nova startup
    path("list/", ListStartups.as_view(), name="list_startups"),#Lista todas as startups
    path("<int:id>/", GetSpecificStartup.as_view(), name="get_startup"),#Retorna os dados de uma startup específica
    path("update/<int:id>/", UpdateStartup.as_view(), name="update_startup"),#Atualiza os dados de uma startup específica
    path("delete/<int:id>/", DeleteStartup.as_view(), name="delete_startup"),#Deleta uma startup :( ainda não sei se vai ser útil, mas um crudzinho é sempre bom
]