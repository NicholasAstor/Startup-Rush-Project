from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.db import connection

import random

from .models import Battle, EventBattle, Event
from startups.models import Startup, StartupStatistics
from tournaments.models import StartupTournament, Round

@csrf_protect
def manage_battle(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)

    # TODO: tenho que fazer a página de gerenciamento de batalhas    
    if battle.status == 'done':
        return JsonResponse({'success': False,'message': 'Esta batalha já terminou'})
    
    events = Event.objects.all()
    
    # Buscar informações de torneio de cada startup
    startup1_tournament = StartupTournament.objects.filter(startup=battle.startup1, tournament=battle.round.tournament).first()
    
    startup2_tournament = StartupTournament.objects.filter(startup=battle.startup2, tournament=battle.round.tournament).first()

    if not startup1_tournament or not startup2_tournament:
        return JsonResponse({'success': False,'message': 'Algum problema no fluxo de torneio.'})
    
    # Pegar os eventos registrados para a batalha e colocar pra cada uma das startups
    battle_events = EventBattle.objects.filter(battle=battle)

    startup1_events = []
    for battleevent in battle_events:
        if battleevent.startup == battle.startup1:
            startup1_events.append(battleevent.event.id)

    startup2_events = []
    for battleevent in battle_events:
        if battleevent.startup == battle.startup2:
            startup2_events.append(battleevent.event.id)
    
    context = {
        'battle': battle,
        'events': events,
        'startup1_tournament': startup1_tournament,
        'startup2_tournament': startup2_tournament,
        'startup1_events': startup1_events,
        'startup2_events': startup2_events,
        'battle_events': battle_events,
    }
    
    return render(request, 'battles/manage_battle.html', context)

@csrf_protect
def add_event(request, battle_id):
    if request.method == 'POST':
        battle = get_object_or_404(Battle, id=battle_id)
        
        # Mesma verificação de antes, futuramente colocar um redirecionamento para a página de gerenciamento de batalhas
        if battle.status == 'done':
            return JsonResponse({'success': False, 'message': 'Esta batalha já terminou'})
        
        startup_id = request.POST.get('startup_id')
        event_id = request.POST.get('event_id')

        #Outras verificações básicas mas que são necessárias
        
        startup = Startup.objects.filter(id=startup_id).first()
        
        if not startup:
            return JsonResponse({'success': False,'message': 'Não foi possível encontrar a startup'})
        
        event = Event.objects.filter(id=event_id).first()
        
        if not event:
            return JsonResponse({'success': False,'message': 'Não foi possível encontrar o evento'})

        if startup != battle.startup1 and startup != battle.startup2:
            return JsonResponse({'success': False,'message': 'Esta startup não faz parte da batalha'})
        
        # Um evento não pode ser registrado mais de uma vez para a mesma startup na mesma batalha
        if EventBattle.objects.filter(battle=battle, startup=startup, event=event).exists():
            return JsonResponse({'success': False,'message': 'Esta startup não pode mais receber esse evento por enquanto'})
        
        # Caso de tudo certo o reistro do evento pra aquela startup vai ser criado
        EventBattle.objects.create(battle=battle,startup=startup,event=event)
        
        # Atualizar pontuação da startup no torneio
        startup_tournament = StartupTournament.objects.filter(startup=startup, tournament=battle.round.tournament).first() #Saudades sql ;(
        startup_tournament.score += event.impact_score
        startup_tournament.save()
        
        # Método auxiliar para atualizar as estatisticas da startup
        update_startup_statistics(startup, event)
        
        return JsonResponse({'success': True,'score': startup_tournament.score,'message': f'Evento "{event.name}" adicionado a {startup.name}'})
    
    else:
        return JsonResponse({'success': False, 'message': 'Requisição inválida'})

def update_startup_statistics(startup, event):
    try:
        #Verifico no banco se já existe um registro das estatísticas dessa startup (já é pra existir) caso não exista eu crio um novo
        stats = StartupStatistics.objects.filter(startup=startup).first()
        
        if not stats:
            stats = StartupStatistics.objects.create(startup=startup)
        
        # Não consegui pensar em um jeito melhor de fazer isso, fiz do jeito de 1 semestre mesmo :)
        if event.name == 'Pitch convincente':
            stats.total_pitches += 1
        elif event.name == 'Produto com bugs':
            stats.total_bugs += 1
        elif event.name == 'Boa tração de usuários':
            stats.total_traction += 1
        elif event.name == 'Investidor irritado':
            stats.total_pissed_investors += 1
        elif event.name == 'Fake news':
            stats.total_fakenews += 1
            
        stats.save()
    except Exception as e:
        print(f"Erro ao atualizar estatísticas: {e}")

@csrf_protect
def complete_battle(request, battle_id):
    if request.method == 'POST':
        battle = get_object_or_404(Battle, id=battle_id)
        
        if battle.status == 'done':
            return JsonResponse({'success': False,'message': 'Esta batalha já terminou'})
        
        # Conseguir as pontuações das startups
        startup1_tournament = StartupTournament.objects.filter(startup=battle.startup1, tournament=battle.round.tournament).first()
        startup2_tournament = StartupTournament.objects.filter(startup=battle.startup2, tournament=battle.round.tournament).first()

        stats1 = StartupStatistics.objects.filter(startup=battle.startup1).first()
        stats2 = StartupStatistics.objects.filter(startup=battle.startup2).first()
        
        # SHARKFIGHT!!!!!!
        if startup1_tournament.score == startup2_tournament.score:
            battle.shark_fight = True
            battle.save()
            
            winner = random.choice([battle.startup1, battle.startup2])
            if winner == battle.startup1:
                startup1_tournament.score += 2
                startup1_tournament.save()
                stats1.total_sharkfights += 1
                stats1.save()
            else:
                startup2_tournament.score += 2
                startup2_tournament.save()
                stats2.total_sharkfights += 1
                stats2.save()

        # Vencedor da batalha
        if startup1_tournament.score > startup2_tournament.score:
            winner = battle.startup1
            startup_winner = startup1_tournament
        else:
            winner = battle.startup2
            startup_winner = startup2_tournament
        
        battle.winner = winner
        battle.status = 'done'
        battle.save()
        
        # Colocar os merecidos 30 pontos da vitória
        startup_winner.score += 30
        startup_winner.save()
        
        #Também atualizar as estatísticas do ganhador
        winner_stats = StartupStatistics.objects.filter(startup=winner).first()
        winner_stats.total_wins += 1
        winner_stats.save()
        
        round_battles = Battle.objects.filter(round=battle.round)

        winners = []
        for b in round_battles:
            if b.winner:
                winners.append(b.winner)
        
        # Verificar se todas as batalhas foram concluídas
        all_completed = False
        for b in round_battles:
            if b.status != 'done':
                all_completed = False
                break
            else:
                all_completed = True
        
        if all_completed == True:
            current_round = Round.objects.filter(id=battle.round.id).first()
            current_round.status = 'done'
            current_round.save()
            
            tournament = current_round.tournament

            round_number = current_round.number

            # Verificação de precisamos criar outra rodada            
            if tournament.qty_rounds > round_number:
                next_round_number = round_number + 1
                next_round = Round.objects.create(tournament=tournament,number=next_round_number,status='ongoing')
                
                # Ah shit here we go again
                random.shuffle(winners)
                caso6 = None
                if len(winners) % 2 != 0:
                    caso6 = winners.pop()

                for i in range(0, len(winners), 2):
                    Battle.objects.create(round=next_round,startup1=winners[i],startup2=winners[i+1],status='pending')
 
                if caso6:
                    Battle.objects.create(round=next_round, startup1=caso6, startup2=None, winner=caso6, status='done')
                    new_score = StartupTournament.objects.filter(startup = caso6, tournament=next_round.tournament).first()
                    new_score.score += 30
                    new_score.save()

            else:
                #FIM DO TORNEIO MEU AMIGOS
                tournament.status = 'done'
                tournament.champion = winners[0]
                tournament.save()
        
        return JsonResponse({'success': True, 'redirect': '/battles/'}) #TODO: fazer tela mostrando as estatísticas de todos os participantes
    
    else:
        return JsonResponse({'success': False, 'message': 'Requisição inválida'})
    
def pending_battles(request): # Tela para exibir todas as batalhas com status pendente
    battles = Battle.objects.filter(status='pending').select_related('startup1', 'startup2', 'round__tournament')
    
    # Conseguir todos os torneios de IDs únicos
    tournament_ids = set()
    for battle in battles:
        tournament_ids.add(battle.round.tournament_id)
    
    tournament_scores = {}    
    # Acessar a pontuação das startups nos torneios específicos
    with connection.cursor() as cursor:
        for tournament_id in tournament_ids:
            cursor.execute("""
                SELECT startup_id, score 
                FROM Startup_tournament 
                WHERE tournament_id = %s
            """, [tournament_id])
            tournament_scores[tournament_id] = dict(cursor.fetchall())
    
    # Vou precisar atualizar o score de cada startup por batalha
    for battle in battles:
        tournament_id = battle.round.tournament_id
        scores = tournament_scores.get(tournament_id, {})
        
        battle.startup1_score = scores.get(battle.startup1_id, 70)
        battle.startup2_score = scores.get(battle.startup2_id, 70)
    
    return render(request, 'battles/pending_battles.html', {'battles': battles,'title': 'Batalhas Pendentes'})