from django.urls import path
from .views import DbTestView

urlpatterns = [
    path("dbtest/", DbTestView.as_view(), name="db_test"),
]