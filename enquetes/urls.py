from django.urls import path
from . import views

app_name = 'enquetes'

urlpatterns = [
    path('', views.index, name='index'),  # página inicial com lista de enquetes
    path('<int:questao_id>/', views.detalhes, name='detalhes'),
    path('<int:questao_id>/voto/', views.voto, name='voto'),
    path('<int:questao_id>/resultados/', views.resultados, name='resultados'),
    path('alternativa/<int:alternativa_id>/excluir/', views.excluir_alternativa, name='excluir_alternativa'),
    path('alternativa/<int:alternativa_id>/editar/', views.editar_alternativa, name='editar_alternativa'),
]