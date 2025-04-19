from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('startups/', views.startups_list, name='startups_list'),
    path('startups/create/', views.create_startup, name='create_startup'),
    path('startups/delete/<int:startup_id>/', views.delete_startup, name='delete_startup'),

    path('results/', views.analyze_results, name='analyze_results'), #TODO
    path('ranking/', views.view_ranking, name='view_ranking'),#TODO
    path('manage_startups/', views.manage_startups, name='manage_startups'),#TODO
]