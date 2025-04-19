from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Startup, StartupStatistics
from .forms import StartupForm

def home(request): #Landing page
    return render(request, 'home.html')

def startups_list(request):#retorna todas as startups ativas e suas devidas estatísticas
    startups = Startup.objects.filter(active=True)
    startupstats = StartupStatistics.objects.filter(startup__in=startups)
    
    context = {'startups': startups,'has_startups': startups.exists(), 'startupstats': startupstats}
    
    return render(request, 'startups/list_startups.html', context)

@csrf_exempt
def create_startup(request): #Cria uma nova startup
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            slogan = data.get('slogan')
            year_foundation = data.get('year_foundation')
            
            if not name or not slogan or not year_foundation:
                return JsonResponse({'success': False,'message': 'Todos os campos são obrigatórios'}, status=400)
            
            startup = Startup(name=name,slogan=slogan, year_foundation=year_foundation, active=True)
            startup.save()
            
            StartupStatistics.objects.create( startup=startup)
            
            return JsonResponse({'success': True,'message': 'Startup criada com sucesso :)','startup':{'id':startup.id,'name':startup.name,'slogan': startup.slogan,'year_foundation':startup.year_foundation}})
        except Exception as e:
            return JsonResponse({'success': False,'message': f'Erro ao criar startup: {str(e)} :('}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)

@require_http_methods(["DELETE"])
def delete_startup(request, startup_id):#Deleta uma startup
    try:
        startup = Startup.objects.filter(id=startup_id).first()
        if not startup:
            return JsonResponse({'success': False, 'message': 'Startup não encontrada'}, status=404)
        startup.delete()
        return JsonResponse({'success': True, 'message': 'startup deletada com sucesso :)'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro ao deletar startup: {str(e)} :('}, status=500)

def manage_startups(request): #TODO
    startups = Startup.objects.all()
    return render(request, 'manage_startups.html', {'startups': startups})

def analyze_results(request): #TODO
    return render(request, 'analyze_results.html')

def view_ranking(request): #TODO
    startups = Startup.objects.all().order_by('-score') 
    return render(request, 'ranking.html', {'startups': startups})