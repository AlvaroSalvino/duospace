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
def desfazer_amizade(request, perfil_id):
    try:
        # Obtém o perfil do usuário que está sendo removido da lista de contatos
        perfil_a_remover = Perfil.objects.get(id=perfil_id)
        perfil_logado = request.user.perfil
        
        # Verifica se o perfil a ser removido está na lista de contatos
        if perfil_a_remover in perfil_logado.contatos.all():
            perfil_logado.desfazer_amizade(perfil_a_remover)
            messages.add_message(request, messages.INFO, f'Amizade com {perfil_a_remover.nome} desfeita.')
        else:
            messages.add_message(request, messages.INFO, 'Este perfil não é seu amigo.')

    except Perfil.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Perfil não encontrado.')

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

def ler_notificacoes(request):
    if request.method == 'POST':
        perfil = request.user.perfil
        perfil.notificacoes.filter(lida=False).update(lida=True)
        return JsonResponse({'status': 'sucesso', 'mensagem': 'Notificações marcadas como lidas.'})
    return JsonResponse({'status': 'erro', 'mensagem': 'Requisição inválida.'}, status=400)