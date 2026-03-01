from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from .models import Questao, Alternativa
from django.contrib import messages
from .forms import AlternativaForm

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

# ====================== EXCLUSÃO ======================
def excluir_alternativa(request, alternativa_id):
    alternativa = get_object_or_404(Alternativa, pk=alternativa_id)
    questao_id = alternativa.questao.id  # para redirecionar de volta

    if request.method == 'POST':
        alternativa.delete()
        messages.success(request, f'Alternativa "{alternativa.texto_alternativa}" excluída com sucesso!')
        return redirect('enquetes:detalhes', questao_id=questao_id)
    
    # GET: confirmação (opcional)
    return render(request, 'enquetes/confirmar_exclusao.html', {'alternativa': alternativa})

# ====================== EDIÇÃO ======================
def editar_alternativa(request, alternativa_id):
    alternativa = get_object_or_404(Alternativa, pk=alternativa_id)
    questao_id = alternativa.questao.id

    if request.method == 'POST':
        form = AlternativaForm(request.POST, instance=alternativa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alternativa atualizada com sucesso!')
            return redirect('enquetes:detalhes', questao_id=questao_id)
    else:
        form = AlternativaForm(instance=alternativa)

    return render(request, 'enquetes/editar_alternativa.html', {
        'form': form,
        'alternativa': alternativa
    })