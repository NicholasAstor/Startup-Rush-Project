from django.urls import path
from . import views

urlpatterns = [ # Todos os endpoints são autoexplicativos aqui :)
    path('', views.home, name='home'), #Eu podia ter botado dentro do app client que é o principal mas preferi por fazer dessa maneira e centralizar melhor as cosas
    path('startups/', views.startups_list, name='startups_list'),
    path('startups/create/', views.create_startup, name='create_startup'),
    path('startups/delete/<int:startup_id>/', views.delete_startup, name='delete_startup'),
]