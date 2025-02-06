from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import *

@login_required(login_url='login')
def alterar_cor(request):
    if request.method == 'POST':
        cor = request.POST.get('cor')
        perfil_logado = request.user.perfil
        perfil_logado.cor = cor
        perfil_logado.save()
        
        # Retornando um JSON para confirmar a mudança
        return JsonResponse({'status': 'success', 'cor': cor})
    return JsonResponse({'status': 'error'})

@login_required(login_url='login')
def alterar_background(request):
    if request.method == 'POST':
        background = request.POST.get('background')
        perfil_logado = request.user.perfil
        perfil_logado.background = background
        perfil_logado.save()
        
        # Retornando um JSON para confirmar a mudança
        return JsonResponse({'status': 'success', 'background': background})
    return JsonResponse({'status': 'error'})

@login_required(login_url='login')
def alterar_fonte(request):
    if request.method == 'POST':
        fonte = request.POST.get('fonte')
        perfil_logado = request.user.perfil
        perfil_logado.fonte = fonte
        perfil_logado.save()
        
        # Retornando um JSON para confirmar a mudança
        return JsonResponse({'status': 'success', 'fonte': fonte})
    return JsonResponse({'status': 'error'})

# Funções soltas
@login_required(login_url='login')
def convidar(request, perfil_id):
    perfil_a_convidar = Perfil.objects.get(id=perfil_id)
    perfil_logado = request.user.perfil
    convite_realizado = Convite.objects.filter(solicitante=perfil_a_convidar, convidado=perfil_logado)

    if convite_realizado:
        messages.add_message(request, messages.INFO, 'Impossível enviar solicitação, há uma solicitação de {} para você'.format(perfil_a_convidar.nome))
    else:
        perfil_logado.convidar(perfil_a_convidar)
        messages.add_message(request, messages.INFO, 'Solicitação de amizade enviada para {}.'.format(perfil_a_convidar.nome))

    return redirect('index')

@login_required(login_url='login')
def aceitar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    messages.add_message(request, messages.INFO, 'Convite aceito para {}.'.format(convite.solicitante.nome))
    convite.aceitar()
    return redirect('index')

@login_required(login_url='login')
def rejeitar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.rejeitar()
    messages.add_message(request, messages.INFO, 'Solicitação cancelada.')
    return redirect('index')