from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib.auth.models import User

def create_perfil(request):
    if request.method == 'POST':
        data = request.POST
        user = get_object_or_404(User, id=data.get('usuario_id'))
        perfil = Perfil.objects.create(
            nome=data.get('nome'),
            telefone=data.get('telefone'),
            usuario=user
        )
        return JsonResponse({'message': 'Perfil criado com sucesso', 'id': perfil.id}, status=201)

def get_perfil(request, perfil_id):
    perfil = get_object_or_404(Perfil, id=perfil_id)
    data = {
        'id': perfil.id,
        'nome': perfil.nome,
        'telefone': perfil.telefone,
        'email': perfil.email,
        'imagem_perfil': perfil.imagem_perfilURL,
        'imagem_capa': perfil.imagem_capaURL,
    }
    return JsonResponse(data)

def update_perfil(request, perfil_id):
    if request.method == 'POST':
        data = request.POST
        perfil = get_object_or_404(Perfil, id=perfil_id)
        perfil.nome = data.get('nome', perfil.nome)
        perfil.telefone = data.get('telefone', perfil.telefone)
        perfil.save()
        return JsonResponse({'message': 'Perfil atualizado com sucesso'})

def delete_perfil(request, perfil_id):
    perfil = get_object_or_404(Perfil, id=perfil_id)
    perfil.delete()
    return JsonResponse({'message': 'Perfil deletado com sucesso'})

def create_post(request):
    if request.method == 'POST':
        data = request.POST
        perfil = get_object_or_404(Perfil, id=data.get('perfil_id'))
        post = Post.objects.create(
            titulo=data.get('titulo'),
            text=data.get('text'),
            perfil=perfil
        )
        return JsonResponse({'message': 'Post criado com sucesso', 'id': post.id}, status=201)

def get_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    data = {
        'id': post.id,
        'titulo': post.titulo,
        'text': post.text,
        'data_postagem': post.data_postagem,
        'perfil': post.perfil.nome,
        'imagem': post.imagemURL,
        'curtidas': post.curtida_set_count
    }
    return JsonResponse(data)

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return JsonResponse({'message': 'Post deletado com sucesso'})

def create_comentario(request):
    if request.method == 'POST':
        data = request.POST
        perfil = get_object_or_404(Perfil, id=data.get('perfil_id'))
        post = get_object_or_404(Post, id=data.get('post_id'))
        comentario = Comentario.objects.create(
            perfil=perfil,
            post=post,
            texto=data.get('texto')
        )
        return JsonResponse({'message': 'Comentário criado com sucesso', 'id': comentario.id}, status=201)

def delete_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    comentario.delete()
    return JsonResponse({'message': 'Comentário deletado com sucesso'})

def curtir_post(request):
    if request.method == 'POST':
        data = request.POST
        perfil = get_object_or_404(Perfil, id=data.get('perfil_id'))
        post = get_object_or_404(Post, id=data.get('post_id'))
        curtida, created = Curtida.objects.get_or_create(perfil=perfil, post=post)
        if not created:
            curtida.delete()
            return JsonResponse({'message': 'Curtida removida'})
        return JsonResponse({'message': 'Post curtido com sucesso'})

def get_notificacoes(request, perfil_id):
    perfil = get_object_or_404(Perfil, id=perfil_id)
    notificacoes = perfil.notificacoes.all().values()
    return JsonResponse(list(notificacoes), safe=False)
