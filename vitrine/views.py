from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from perfil.models import *
from django.contrib import messages
from django.utils.timesince import timesince
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage

@login_required(login_url='login')
def index(request):
    user = request.user
    perfil = get_object_or_404(Perfil, usuario=user)
    context = {
        'active_home': 'active',
    }
    context['perfis'] = Perfil.objects.all()
    context['perfil_logado'] = request.user.perfil
    context['cor'] = request.user.perfil.cor
    context['fonte'] = request.user.perfil.fonte
    context['background'] = request.user.perfil.background
    timeline = selecionar_posts(request)
    
    # Adicionar tempo decorrido aos posts
    for post in timeline:
        post.tempo_decorrido = timesince(post.data_postagem)  # Exemplo: "2 horas, 15 minutos"
        
    paginator = Paginator(timeline, 15)
    page = request.GET.get('pagina')

    try:
        context['timeline'] = paginator.page(page)
    except Exception:
        context['timeline'] = paginator.page(1)
        if page is not None:
            messages.add_message(request, messages.INFO, 'A página {} não existe'.format(page))
    
    if request.method == "POST":
        # Verifica e salva a foto se fornecida
        if 'imagem_perfil' in request.FILES:
            perfil.imagem_perfil = request.FILES['imagem_perfil']
            perfil.save()  # Salva no banco de dados

    return render(request, 'index.html', context)

def selecionar_posts(request):
    perfil_logado = request.user.perfil
    amigos = perfil_logado.contatos.all()
    posts = list(perfil_logado.posts.all())  # Adiciona os posts do próprio usuário
    for amigo in amigos:
        posts.extend(list(amigo.posts.all()))
    posts.sort(key=lambda x: x.data_postagem, reverse=True)
    return posts

@login_required(login_url='login')
def buscar_usuario(request):
    encontrados = Perfil.objects.all()
    if request.method == 'POST':
        query = request.POST.get('busca')

        if len(query) <= 0:
            messages.add_message(request, messages.INFO, 'Digite algo no campo de busca.')
            return redirect('index')

        encontrados = list(Perfil.objects.filter(nome__contains=query))
        if request.user.perfil in encontrados:
            encontrados.remove(request.user.perfil)

    context = {}
    context['cor'] = request.user.perfil.cor
    context['fonte'] = request.user.perfil.fonte
    context['background'] = request.user.perfil.background
    context['encontrados'] = encontrados
    context['perfil_logado'] = request.user.perfil
        
    return render(request, 'buscarusuario.html', context)

@login_required(login_url='login')
def postagem(request):
    if request.method == 'POST':
        try:
            titulo = request.POST.get('titulo')
            texto = request.POST.get('texto')
            imagem = request.FILES['imagem']
            perfil = request.user.perfil

            postagem_valida = True
            if len(titulo) <= 0:
                messages.add_message(request, messages.INFO, 'O campo de título deve ser preenchido.')
                postagem_valida = False
            if len(texto) <= 0:
                messages.add_message(request, messages.INFO, 'O campo de texto deve ser preenchido.')
                postagem_valida = False
            if not postagem_valida:
                return redirect('index')
            else:
                # Formatação da imagem
                file_system = FileSystemStorage()
                file_name = file_system.save(imagem.name, imagem)
                # Salvando no banco de dados
                Post.objects.create(titulo=titulo, text=texto, perfil=perfil, imagem=file_name)
                messages.add_message(request, messages.INFO, 'Postagem publicada.')

        except Exception:
            titulo = request.POST.get('titulo')
            texto = request.POST.get('texto')

            postagem_valida = True
            if len(titulo) <= 0:
                messages.add_message(request, messages.INFO, 'O campo de título deve ser preenchido.')
                postagem_valida = False
            if len(texto) <= 0:
                messages.add_message(request, messages.INFO, 'O campo de texto deve ser preenchido.')
                postagem_valida = False
            if not postagem_valida:
                return redirect('index')
            else:
                perfil = request.user.perfil
                Post.objects.create(titulo=titulo, text=texto, perfil=perfil)
                messages.add_message(request, messages.INFO, 'Postagem publicada.')

    return redirect('index')

@login_required(login_url='login')
def exibir_perfil(request, perfil_id):
    context = {}
    context['cor'] = request.user.perfil.cor
    context['fonte'] = request.user.perfil.fonte
    context['background'] = request.user.perfil.background
    context['perfil'] = Perfil.objects.get(id=perfil_id)
    context['perfil_logado'] = perfil_logado = request.user.perfil
    context['ja_eh_contato'] = context['perfil_logado'].contatos.filter(id=context['perfil'].id)
    context['timeline'] = context['perfil'].posts.all() 

    return render(request, 'perfil.html', context)