from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('salvos/', marcados, name='marcados'),
    path('encontrar/', buscar_usuario, name='buscar_usuario'),
    path('postagem/', postagem, name='postagem'),
    path('perfil/<int:perfil_id>/', exibir_perfil, name='exibir'),
    path('deletepostagem/<int:id_postagem>', delete_postagem, name='delete_postagem'),
    path('curtir/<int:post_id>/', curtir_post, name='curtir_post'),
    path('curtir-comentario/<int:comentario_id>/', curtir_comentario, name='curtir_comentario'),
    path('marcar/<int:post_id>/', marcar_post, name='marcar_post'),
    path('post/<int:post_id>/comentar/', adicionar_comentario, name='adicionar_comentario'),
    path('comentarios/<int:post_id>/', listar_comentarios, name='listar_comentarios'),
    path('post/<int:post_id>/', ver_post, name='ver_post'),
    path('post-comentario/<int:comentario_id>/', ver_post_comentario, name='ver_post_comentario'),
]