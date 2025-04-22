from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

from .models import Startup, StartupStatistics

def home(request): #Landing page
    return render(request, 'home.html')

def startups_list(request):#retorna todas as startups
    startups = Startup.objects.all()
    
    return render(request, 'startups/list_startups.html', {'startups': startups})

@csrf_exempt
def create_startup(request): #Cria uma nova startup
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            slogan = data.get('slogan')
            year_foundation = data.get('year_foundation')
            
            if not name or not slogan or not year_foundation: # Sempre vou fazer uma verificação inicial  para evitar erros na logica
                return JsonResponse({'success': False,'message': 'É necessário preencher todos os campos'}, status=400)
            
            startup = Startup.objects.create(name=name,slogan=slogan, year_foundation=year_foundation, active=True)
            
            StartupStatistics.objects.create( startup=startup)
            
            return JsonResponse({'success': True,'message': 'Startup criada com sucesso :)',})
        except Exception as e:
            return JsonResponse({'success': False,'message': f'Erro na criação da startup: {str(e)} :('}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)

def delete_startup(request, startup_id):#Deleta uma startup
    if request.method == 'DELETE':
        try:
            startup = Startup.objects.filter(id=startup_id).first()
            if not startup:
                return JsonResponse({'success': False, 'message': 'Não foi possível encontrar a startup'}, status=404)
            startup.delete()
            return JsonResponse({'success': True, 'message': 'startup deletada com sucesso :)'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro em deletar startup: {str(e)} :('}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)