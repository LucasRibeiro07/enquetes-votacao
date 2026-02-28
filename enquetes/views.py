from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from .models import Questao, Alternativa

def index(request):
    ultimas_questoes = Questao.objects.order_by('-data_publicacao')[:5]
    return render(request, 'enquetes/index.html', {'ultimas_questoes': ultimas_questoes})

def detalhes(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'enquetes/detalhes.html', {'questao': questao})

def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        selecionada = questao.alternativa_set.get(pk=request.POST['alternativa'])
    except (KeyError, Alternativa.DoesNotExist):
        return render(request, 'enquetes/detalhes.html', {
            'questao': questao,
            'error_message': "Você não selecionou uma alternativa.",
        })
    else:
        selecionada.votos = F('votos') + 1
        selecionada.save()
        return HttpResponseRedirect(reverse('enquetes:resultados', args=(questao.id,)))

def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'enquetes/resultados.html', {'questao': questao})