from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from perfil.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.timesince import timesince
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage

@login_required(login_url='login')
def index(request):
    user = request.user
    perfil = get_object_or_404(Perfil, usuario=user)
    notificacoes = Notificacao.objects.filter(perfil_notificado=perfil).order_by('-data_criacao')

    context = {
        'active_home': 'active',
        'perfis': Perfil.objects.all(),
        'perfil_logado': perfil,
        'cor': perfil.cor,
        'fonte': perfil.fonte,
        'background': perfil.background,
        'notificacoes':notificacoes,
    }

    timeline = selecionar_posts(request)

    # Adicionar status de curtida a cada post
    for post in timeline:
        post.tempo_decorrido = timesince(post.data_postagem)
        post.curtido = Curtida.objects.filter(perfil=perfil, post=post).exists()  # Verifica se foi curtido
        post.marcado = Marcador.objects.filter(perfil=perfil, post=post).exists  # Verifica se foi marcado

    paginator = Paginator(timeline, 5)
    page = request.GET.get('pagina')

    try:
        context['timeline'] = paginator.page(page)
    except Exception:
        context['timeline'] = paginator.page(1)
        if page is not None:
            messages.add_message(request, messages.INFO, 'A página {} não existe'.format(page))
    
    if request.method == "POST":
        if 'imagem_perfil' in request.FILES:
            perfil.imagem_perfil = request.FILES['imagem_perfil']
            perfil.save() 

    return render(request, 'index.html', context)

@login_required(login_url='login')
def carregar_posts(request):
    if request.method == "GET":
        pagina = int(request.GET.get('pagina', 1))  # Obtém a página a ser carregada
        posts_por_pagina = 5

        user = request.user
        perfil = get_object_or_404(Perfil, usuario=user)
        timeline = selecionar_posts(request)

        for post in timeline:
            post.tempo_decorrido = timesince(post.data_postagem)
            post.curtido = Curtida.objects.filter(perfil=perfil, post=post).exists()
            post.marcado = Marcador.objects.filter(perfil=perfil, post=post).exists()

        paginator = Paginator(timeline, posts_por_pagina)
        try:
            posts_pagina = paginator.page(pagina)
        except:
            return JsonResponse({"posts": []})  # Retorna uma lista vazia se a página não existir

        posts_lista = []
        for post in posts_pagina:
            posts_lista.append({
                "id": post.id,
                "titulo": post.titulo,
                "tempo_decorrido": post.tempo_decorrido,
                "data_postagem": post.data_postagem.strftime("%d/%m/%Y %H:%M"),
                "imagem": post.imagem.url if post.imagem else None,
                "perfil": {
                    "nome": post.perfil.nome,
                    "imagem_perfil": post.perfil.imagem_perfil.url if post.perfil.imagem_perfil else None
                },
                "texto": post.text,
                "curtido": post.curtido,
                "marcado": post.marcado,
                "comentarios_count": post.comentarios.count(),
            })

        return JsonResponse({"posts": posts_lista})
    
def selecionar_posts(request):
    perfil_logado = request.user.perfil
    amigos = perfil_logado.contatos.all()
    posts = list(perfil_logado.posts.all())  # Adiciona os posts do próprio usuário
    for amigo in amigos:
        posts.extend(list(amigo.posts.all()))
    posts.sort(key=lambda x: x.data_postagem, reverse=True)
    return posts

def numero_notificacoes(request):
    if request.user.is_authenticated:
        perfil = request.user.perfil
        notificacoes_nao_lidas = Notificacao.objects.filter(perfil_notificado=perfil, lida=False).count()
    else:
        notificacoes_nao_lidas = 0

    return {'notificacoes_nao_lidas': notificacoes_nao_lidas}

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

@login_required(login_url='login')
def ver_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    perfil = get_object_or_404(Perfil, usuario=user)
    notificacoes = Notificacao.objects.filter(perfil_notificado=perfil).order_by('-data_criacao')

    
    post.tempo_decorrido = timesince(post.data_postagem)
    post.curtido = Curtida.objects.filter(perfil=perfil, post=post).exists()  # Verifica se foi curtido

    if request.method == "POST":
        if 'imagem_perfil' in request.FILES:
            perfil.imagem_perfil = request.FILES['imagem_perfil']
            perfil.save() 

    context = {
        'post':post,
        'perfil_logado': perfil,
        'cor': perfil.cor,
        'fonte': perfil.fonte,
        'background': perfil.background,
        'notificacoes':notificacoes,
    }
    return render(request, 'post.html', context)

@login_required(login_url='login')
def delete_postagem(request, id_postagem):
    post = Post.objects.get(id=id_postagem)

    if post.perfil == request.user.perfil or request.user.is_superuser:
        post.delete()
        messages.add_message(request, messages.INFO, 'Post deletado com sucesso!')

    return redirect('index')

@login_required(login_url='login')
def curtir_post(request, post_id):
    post = Post.objects.get(id=post_id)
    perfil = request.user.perfil

    # Tenta obter ou criar a "curtida"
    curtida, created = Curtida.objects.get_or_create(perfil=perfil, post=post)

    if not created:
        curtida.delete()
        status = 'descurtido'
    else:
        status = 'curtido'

    # Corrigir para usar o related_name 'curtidas'
    return JsonResponse({
        'status': status,
        'likes': post.curtidas.count(),
        'liked': created  # 'liked' será True se o post foi curtido, False se descurtado
    })

@login_required
def adicionar_comentario(request, post_id):
    if request.method == "POST":
        texto = request.POST.get("texto")
        if texto.strip():  # Verifica se o texto não está vazio
            post = get_object_or_404(Post, id=post_id)
            perfil = request.user.perfil  # Obtém o perfil do usuário autenticado

            comentario = Comentario.objects.create(perfil=perfil, post=post, texto=texto)
            comentario.save()

            return JsonResponse({"status": "success", "mensagem": "Comentário adicionado com sucesso!"})
        else:
            return JsonResponse({"status": "error", "mensagem": "O comentário não pode estar vazio."})
    
    return JsonResponse({"status": "error", "mensagem": "Requisição inválida."})

@login_required
def listar_comentarios(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comentarios = Comentario.objects.filter(post=post).order_by('-data_comentario')

    comentarios_json = [
        {
            "perfil": comentario.perfil.usuario.username,
            "imagem_perfil": comentario.perfil.imagem_perfil.url if comentario.perfil.imagem_perfil else "/static/assets/images/img/user.png",
            "texto": comentario.texto,
            "data": timesince(comentario.data_comentario) + " atrás"
        }
        for comentario in comentarios
    ]

    return JsonResponse({"comentarios": comentarios_json})

@login_required(login_url='login')
def marcar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    perfil = get_object_or_404(Perfil, usuario=request.user)

    marcador, created = Marcador.objects.get_or_create(perfil=perfil, post=post)

    if not created:
        marcador.delete()
        status = 'desmarcado'
    else:
        status = 'marcado'

    return JsonResponse({
        'status': status,
        'marcado': created,
    })

@login_required(login_url='login')
def marcados(request):
    user = request.user
    perfil = get_object_or_404(Perfil, usuario=user)
    notificacoes = Notificacao.objects.filter(perfil_notificado=perfil).order_by('-data_criacao')

    context = {
        'active_marcados': 'active',
        'perfis': Perfil.objects.all(),
        'perfil_logado': perfil,
        'cor': perfil.cor,
        'fonte': perfil.fonte,
        'background': perfil.background,
        'notificacoes':notificacoes,
    }

    timeline = selecionar_posts_marcados(request)

    # Adicionar status de curtida a cada post
    for post in timeline:
        post.tempo_decorrido = timesince(post.data_postagem)
        post.curtido = Curtida.objects.filter(perfil=perfil, post=post).exists()  # Verifica se foi curtido
        post.marcado = Marcador.objects.filter(perfil=perfil, post=post).exists  # Verifica se foi marcado

    paginator = Paginator(timeline, 15)
    page = request.GET.get('pagina')

    try:
        context['timeline'] = paginator.page(page)
    except Exception:
        context['timeline'] = paginator.page(1)
        if page is not None:
            messages.add_message(request, messages.INFO, 'A página {} não existe'.format(page))
    
    if request.method == "POST":
        if 'imagem_perfil' in request.FILES:
            perfil.imagem_perfil = request.FILES['imagem_perfil']
            perfil.save() 

    return render(request, 'marcados.html', context)

def selecionar_posts_marcados(request):
    perfil_logado = request.user.perfil
    marcadores = Marcador.objects.filter(perfil=perfil_logado)  # Filtra os posts marcados pelo usuário
    posts = [marcador.post for marcador in marcadores]  # Obtém os posts marcados

    # Ordena os posts pela data de postagem (mais recentes primeiro)
    posts.sort(key=lambda x: x.data_postagem, reverse=True)

    return posts
