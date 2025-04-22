from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

import json
import random

from startups.models import Startup
from .models import Tournament, StartupTournament
from battles.models import Battle, Round

def list_tournaments(request): #listar os torneios
    tournaments = Tournament.objects.all().order_by('-id')
    startups = Startup.objects.filter(active=True)
    
    return render(request, 'tournaments/list_tournaments.html', {'tournaments': tournaments, 'startups': startups})

@csrf_exempt
def create_tournament(request): #Criação de torneios e divisão de batalhas com suas devidas startups
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qty_startups = int(data['qty_startups'])
            
            if qty_startups < 4 or qty_startups % 2 != 0 or qty_startups > 8: #Verificações necessarias para dependendo da quantidade de startups no torneio
                return JsonResponse({'success': False, 'message': 'um torneio tem que ser formado por 4, 6 ou 8 startups'}, status=400)
            
            if len(data['startups']) != qty_startups:
                return JsonResponse({'success': False, 'message': f'Selecione {qty_startups} startups'}, status=400)
            
            if qty_startups == 4: # Calculo da quantidade de rodadas necessárias 
                qty_rounds = 2
            elif qty_startups == 6 or qty_startups == 8:
                qty_rounds = 3
            else:
                return JsonResponse({'success': False, 'message': 'Quantidade inválida'}, status=400)
            
            #Criação de fato do torneio
            tournament = Tournament.objects.create(qty_startups=qty_startups,qty_rounds=qty_rounds, status='ongoing')
            
            startup_ids = data['startups']

            for startup_id in startup_ids: # Crio cada uma das startups no torneio, com a pontuação inicial padrão
                StartupTournament.objects.create( startup_id=startup_id,tournament=tournament,score=70 )
            
            # Também preciso criar as rodadas e batalhas
            round_1 = Round.objects.create(tournament=tournament,number=1, status='pending')
            
            startups = list(startup_ids) #Transformei em lista pra conseguir embaralhar de forma mais fácil
            random.shuffle(startups)
            
            for i in range(0, len(startups), 2): #Crio as batalhas conforme os requisitos do torneio (2 por batalha)
                Battle.objects.create(round=round_1,startup1_id=startups[i], startup2_id=startups[i+1], status='pending')
            
            return JsonResponse({'success': True,'message': 'Torneio criado com sucesso :)', 'tournament_id': tournament.id,'round_id': round_1.id, 'battles_created': qty_startups // 2})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro ao criar torneio: {str(e)} :('}, status=500)
    
    else:
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)

def tournament_detail(request, tournament_id): #Retorna os dados de um torneio especifico, suas batalhas pontuações participantes rodadas etc...
    tournament = get_object_or_404(Tournament, id=tournament_id)
    
    rounds = Round.objects.filter(tournament=tournament).order_by('number')

    # Tava com saudade de SQL (mentira), não consegui fazer com ORM então pra não perder tempo optei por só fazer com sql puro mesmo, tudo que estava envolvendo a tabela startup_tournament
    # tava dando ruim, por não ter um id como todas as outras (o django sempre tenta forçar a tabela a ter um id) eu de teimoso deixei desse jeito mas sei que teria um jeito melhor
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT startup_id, score 
            FROM Startup_tournament 
            WHERE tournament_id = %s
        """, [tournament_id])
        scores = dict(cursor.fetchall())
    
    com_batalhas = []
    for round in rounds:
        battles = Battle.objects.filter(round=round).select_related('startup1', 'startup2')
        
        com_score = []
        for battle in battles: #Consigo pegar as batalhas e as startups participantes com seus pontos
            battle.startup1_score = scores.get(battle.startup1_id, 70)
            battle.startup2_score = scores.get(battle.startup2_id, 70)
            com_score.append(battle)
        
        com_batalhas.append({'object': round, 'battles': com_score})
    
    participants = []
    #Tentei 20 vezes fazer com ORM e não deu, tive que apelar pro SQL puro :)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT s.id, s.name, st.score, stats.total_wins, stats.total_pitches, stats.total_bugs, stats.total_traction
            FROM Startup_tournament st
            JOIN Startup s ON st.startup_id = s.id
            JOIN Startup_Statistics stats ON s.id = stats.startup_id
            WHERE st.tournament_id = %s
            ORDER BY st.score DESC
        """, [tournament_id])
        for row in cursor.fetchall(): #Aqui tive que fazer um SQL mais completo para conseguir puxar as estatisticas das startups junto (inclusive fiz primeiro o SQL no DBeaver pra depois dar um ctrl+c ctrl+v aqui)
            participants.append({
                'startup': {
                    'id': row[0],
                    'name': row[1],
                    'startupstatistics': {
                        'total_wins': row[3],
                        'total_pitches': row[4],
                        'total_bugs': row[5],
                        'total_traction': row[6]
                    }
                },
                'score': row[2]
            })
    
    return render(request, 'tournaments/tournament_detail.html', {'tournament': tournament,'rounds': com_batalhas,'participants': participants})