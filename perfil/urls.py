from django.urls import path
from .views import *

urlpatterns = [
    path('alterarcor/', alterar_cor, name='alterar_cor'),
    path('alterarbackground/', alterar_background, name='alterar_background'),
    path('alterarfonte/', alterar_fonte, name='alterar_fonte'),
    path('perfil/<int:perfil_id>/convidar/', convidar, name='convidar'),
    path('perfil/<int:convite_id>/aceitar/', aceitar, name='aceitar'),
    path('perfil/<int:convite_id>/rejeitar/', rejeitar, name='rejeitar'),
    path('ler_notificacoes/', ler_notificacoes, name='ler_notificacoes'),
]