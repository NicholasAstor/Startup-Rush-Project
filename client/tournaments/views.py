from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random

from django.db import transaction
from startups.models import Startup
from .models import Tournament, StartupTournament
from rounds.models import Round 
from battles.models import Battle

def list_tournaments(request): #Lisat os torneios
    tournaments = Tournament.objects.all().order_by('-id')
    startups = Startup.objects.filter(active=True)
    
    tournaments_data = []
    for tournament in tournaments:
        champion_name = tournament.champion.name if tournament.champion else None
        tournaments_data.append({'tournament': tournament,'champion_name': champion_name})
    
    return render(request, 'tournaments/list_tournaments.html', {'tournaments': tournaments, 'startups': startups})

@csrf_exempt
@transaction.atomic
def create_tournament(request): #Criação de torneios e divisão de batalhas com suas devidas startups
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qty_startups = int(data['qty_startups'])
            
            if qty_startups not in [4, 6, 8]:
                return JsonResponse({'success': False,'message': 'um torneio só pode possui 4, 6 ou 8 startups'}, status=400)
            
            if len(data['startups']) != qty_startups:
                return JsonResponse({'success': False, 'message': f'Selecione exatamente {qty_startups} startups'}, status=400)
            
            qty_rounds = 2 if qty_startups == 4 else 3 if qty_startups == 6 else 4
            
            tournament = Tournament.objects.create(qty_startups=qty_startups,qty_rounds=qty_rounds, status='ongoing')
            
            startup_ids = data['startups']
            for startup_id in startup_ids:
                StartupTournament.objects.create( startup_id=startup_id,tournament=tournament,score=70 )
            
            round_1 = Round.objects.create(tournament=tournament,number=1, status='pending')
            
            shuffled_startups = list(startup_ids)
            random.shuffle(shuffled_startups)
            
            for i in range(0, len(shuffled_startups), 2):
                Battle.objects.create(round=round_1,startup1_id=shuffled_startups[i], startup2_id=shuffled_startups[i+1], status='pending')
            
            return JsonResponse({'success': True,'message': 'Torneio criado com sucesso :)', 'tournament_id': tournament.id,'round_id': round_1.id, 'battles_created': qty_startups // 2})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro ao criar torneio: {str(e)} :('}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)