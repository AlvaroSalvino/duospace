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

    paginator = Paginator(timeline, 50)
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

def selecionar_posts(request):
    perfil_logado = request.user.perfil
    amigos = perfil_logado.contatos.all()
    posts = list(perfil_logado.posts.all())
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
            imagem = request.FILES.get('imagem')  # Usando .get() para evitar KeyError se não houver imagem

            # Verificar se ao menos um campo foi preenchido
            if not (titulo or imagem):
                messages.add_message(request, messages.INFO, 'Algum campo deve ser preenchido.')
                return redirect('index')

            perfil = request.user.perfil

            # Se imagem foi enviada, trata a imagem
            if imagem:
                file_system = FileSystemStorage()
                file_name = file_system.save(imagem.name, imagem)
                # Criar postagem com imagem
                Post.objects.create(titulo=titulo, text=texto, perfil=perfil, imagem=file_name)
            else:
                # Criar postagem sem imagem
                Post.objects.create(titulo=titulo, text=texto, perfil=perfil)

            messages.add_message(request, messages.INFO, 'Postagem publicada.')

        except Exception as e:
            # Se houver algum erro, enviar uma mensagem para o usuário (opcional)
            messages.add_message(request, messages.ERROR, 'Erro ao publicar a postagem.')
            print(f"Erro: {e}")

    return redirect('index')

@login_required(login_url='login')
def exibir_perfil(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    context = {}
    context['cor_perfil'] = perfil.cor
    context['cor'] = request.user.perfil.cor
    context['fonte_perfil'] = perfil.fonte
    context['fonte'] = request.user.perfil.fonte
    context['background_perfil'] = perfil.background
    context['background'] = request.user.perfil.background
    context['perfil'] = Perfil.objects.get(id=perfil_id)
    context['perfil_logado'] = perfil_logado = request.user.perfil
    context['ja_eh_contato'] = context['perfil_logado'].contatos.filter(id=context['perfil'].id)
    context['timeline'] = context['perfil'].posts.all().order_by('-data_postagem')

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
def ver_post_comentario(request, comentario_id):
    comentario = Comentario.objects.get(id=comentario_id)  # Obtém o comentário pelo ID
    post = comentario.post  # Obtém o post relacionado ao comentário
    user = request.user
    perfil = get_object_or_404(Perfil, usuario=user)
    notificacoes = Notificacao.objects.filter(perfil_notificado=perfil).order_by('-data_criacao')

    # Adiciona os atributos do post
    post.tempo_decorrido = timesince(post.data_postagem)
    post.curtido = Curtida.objects.filter(perfil=perfil, post=post).exists()  # Verifica se foi curtido

    # Se houver uma imagem no perfil, atualiza
    if request.method == "POST":
        if 'imagem_perfil' in request.FILES:
            perfil.imagem_perfil = request.FILES['imagem_perfil']
            perfil.save()

    context = {
        'post': post,  # Passa o post para o template
        'perfil_logado': perfil,
        'cor': perfil.cor,
        'fonte': perfil.fonte,
        'background': perfil.background,
        'notificacoes': notificacoes,
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

@login_required(login_url='login')
def curtir_comentario(request, comentario_id):
    comentario = Comentario.objects.get(id=comentario_id)
    perfil = request.user.perfil

    # Tenta obter ou criar a "curtida"
    curtida, created = Curtida_comentario.objects.get_or_create(perfil=perfil, comentario=comentario)

    if not created:
        curtida.delete()
        status = 'descurtido'
    else:
        status = 'curtido'

    # Corrigir para usar o related_name 'curtidas'
    return JsonResponse({
        'status': status,
        'likes': comentario.curtidas_comentarios.count(),
        'liked': created
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

    # Obter o perfil do usuário logado
    usuario_logado = request.user.perfil

    comentarios_json = [
        {
            "perfil": comentario.perfil.usuario.username,
            "imagem_perfil": comentario.perfil.imagem_perfil.url if comentario.perfil.imagem_perfil else "/static/assets/images/img/user.png",
            "texto": comentario.texto,
            "id": comentario.id,
            "data": timesince(comentario.data_comentario) + " atrás",
            # Adicionar se o comentário foi curtido pelo usuário logado
            "curtido": Curtida_comentario.objects.filter(perfil=usuario_logado, comentario=comentario).exists()
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
