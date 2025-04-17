from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *

from django.shortcuts import render

class DbTestView(APIView):
    def post(self, request):
        name = request.data.get('name')
        slogan = request.data.get('slogan')
        year_foundation = request.data.get('year_foundation')
        score = request.data.get('score')
        active = request.data.get('active')

        if not score:
            score = 70

        if not active:
            active = True

        startup = Startup.objects.create(
            name=name,
            slogan=slogan,
            year_foundation=year_foundation,
            score=score,
            active=active
        )

        return Response({"id": startup.id}, status=status.HTTP_201_CREATED)