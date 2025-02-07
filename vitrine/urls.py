from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('encontrar/', buscar_usuario, name='buscar_usuario'),
    path('postagem/', postagem, name='postagem'),
    path('perfil/<int:perfil_id>/', exibir_perfil, name='exibir'),
    path('deletepostagem/<int:id_postagem>', delete_postagem, name='delete_postagem'),
    path('curtir/<int:id_postagem>/', curtir_post, name='curtir_post'),
    path('post/<int:post_id>/comentar/', adicionar_comentario, name='adicionar_comentario'),
]