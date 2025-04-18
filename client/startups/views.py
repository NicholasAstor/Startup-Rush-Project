from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *

from django.shortcuts import render

class CreateStartup(APIView):
    def post(self, request):
        name = request.data.get('name')
        slogan = request.data.get('slogan')
        year_foundation = request.data.get('year_foundation')

        startup = Startup.objects.create(
            name=name,
            slogan=slogan,
            year_foundation=year_foundation,
            score=70,
            active=True
        )

        return Response({"success":True, "error":False, "message":"success", "data":{"id":startup.id, "name":name}}, status=status.HTTP_201_CREATED)
    
class ListStartups(APIView):
    def get(self, request):
        startups = Startup.objects.all()
        
        startups_serializer = StartupSerializer(startups, many=True)

        return Response({"success":True, "error":False, "message":"success", "data":{"Startups":startups_serializer.data}}, status=status.HTTP_200_OK)
    
class GetSpecificStartup(APIView):
    def get(self, request, *args, **kwargs):
        startup_id = kwargs.get('id')

        if not startup_id:
            return Response({"success":False, "error":True, "message":"Startup ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        startup = Startup.objects.filter(id=startup_id).first()
        if not startup:
            return Response({"success":False, "error":True, "message":"Startup not found"}, status=status.HTTP_404_NOT_FOUND)
        
        startup_serializer = StartupSerializer(startup)
        return Response({"success":True, "error":False, "message":"success", "data":{"Startup":startup_serializer.data}}, status=status.HTTP_200_OK)
    
class UpdateStartup(APIView):
    def put(self, request, *args, **kwargs):
        startup_id = kwargs.get('id')
        
        name = request.data.get('name')
        slogan = request.data.get('slogan')
        year_foundation = request.data.get('year_foundation')

        if not startup_id:
            return Response({"success":False, "error":True, "message":"Startup ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        startup = Startup.objects.filter(id=startup_id).first()
        if not startup:
            return Response({"success":False, "error":True, "message":"Startup not found"}, status=status.HTTP_404_NOT_FOUND)
        
        startup.name = name
        startup.slogan = slogan
        startup.year_foundation = year_foundation
        startup.save()

        return Response({"success":True, "error":False, "message":"Startup updated successfully"}, status=status.HTTP_200_OK)
    
class DeleteStartup(APIView):
    def delete(self, request, *args, **kwargs):
        startup_id = kwargs.get('id')

        if not startup_id:
            return Response({"success":False, "error":True, "message":"Startup ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        startup = Startup.objects.filter(id=startup_id).first()
        if not startup:
            return Response({"success":False, "error":True, "message":"Startup not found"}, status=status.HTTP_404_NOT_FOUND)
        
        startup.delete()
        return Response({"success":True, "error":False, "message":"Startup deleted successfully"}, status=status.HTTP_200_OK)