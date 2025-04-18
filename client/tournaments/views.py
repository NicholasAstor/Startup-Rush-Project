from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render

from .models import Tournament
from .serializers import TournamentSerializer

from startups.models import Startup
from battles.models import Battle
from rounds.models import Round

import random

class CreateTournament(APIView):
    def post(self, request):
        qty_startups = request.data.get('qty_startups')
        
        if not qty_startups:
            return Response({"success":False, "error":True, "message":"Quantity of startups is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            qty_startups = int(qty_startups)
        
        if qty_startups < 4 or qty_startups % 2 !=0 or qty_startups > 8:
            return Response({"success":False, "error":True, "message":"Quantity of startups must be 4, 6 or 8"}, status=status.HTTP_400_BAD_REQUEST)
        
        match qty_startups:
            case 4:
                qty_rounds = 2
            case 6:
                qty_rounds = 3
            case 8:
                qty_rounds = 4
        
        tournament = Tournament.objects.create(
            qty_startups=qty_startups,
            qty_rounds=qty_rounds,
            status='ongoing'
        )

        return Response({"success":True, "error":False, "message":"success", "data":{"id":tournament.id}}, status=status.HTTP_201_CREATED)

class StartTournament(APIView):
    def post(self, request, *args, **kwargs):
        tournament_id = kwargs.get('id')

        if not tournament_id:
            return Response({"success":False, "error":True, "message":"Tournament ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        tournament = Tournament.objects.filter(id=tournament_id).first()

        if not tournament:
            return Response({"success":False, "error":True, "message":"Tournament not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if tournament.status != 'ongoing':
            return Response({"success":False, "error":True, "message":"Tournament is not ongoing"}, status=status.HTTP_400_BAD_REQUEST)
        
        startups = list(Startup.objects.filter(active=True))
        if len(startups) < tournament.qty_startups:
            return Response({"success":False, "error":True, "message":"Not enough startups to start the tournament"}, status=status.HTTP_400_BAD_REQUEST)
        
        selected_startups = random.sample(startups, tournament.qty_startups)

        random.shuffle(selected_startups)

        round = Round.objects.create(
            tournament=tournament,
            number=1,
            status='ongoing'
        )

        for i in range(0, len(selected_startups), 2):
            battle = Battle.objects.create(
                startup1=selected_startups[i],
                startup2=selected_startups[i+1],
                round=round,
                status='pending'
            )

        tournament.status = 'ongoing'
        tournament.save()
        return Response({"success":True, "error":False, "message":"Tournament started successfully"}, status=status.HTTP_200_OK)
