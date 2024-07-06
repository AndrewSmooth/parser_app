from crypt import methods
from django.http import Http404
from django.shortcuts import render

from .api_parser import HhParser

from .models import Vacancy

def index(request):
    parser = HhParser()
    areas = parser.getAreas()
    context = {
        'employment': parser.getEmployment(),
        'experience': parser.getExperience(),
        'areas': areas,
        'profRoles': parser.getProfRoles(),
    }
    return render(request, 'main/index.html', context)
    

def parsing(request):
    if request.POST:
        notFound = False
        parser = HhParser()
        params = [request.POST.get('employment'), request.POST.get('experience'), request.POST.get('area'), request.POST.get('profRole')]
        results = parser.parse(params[0], params[1], params[2], params[3])
        if len(results) > 0:
            Vacancy.objects.all().delete()
            for result in results:
                Vacancy.objects.create(name=result[0], address=result[1], employer=result[2], salary=result[3], employment=result[4], experience=result[5], area=result[6], profRole=result[7])
            
            vacancies = Vacancy.objects.all()

            context = {
                'notFound': False,
                'vacancies': vacancies,
                'count': vacancies.count()
            }
        else:
            context = {
                'notFound': True
            }
        return render(request, 'main/result.html', context)
    else:
        vacancies = Vacancy.objects.filter(employer=request.GET.get('order_by').replace('*', ' '))
        context = {
            'current_filter': request.GET.get('order_by'),
            'vacancies': vacancies,
            'count': vacancies.count(),
        }
        return render(request, 'main/result.html', context)
    
