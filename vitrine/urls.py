from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('encontrar/', buscar_usuario, name='buscar_usuario'),
    path('postagem/', postagem, name='postagem'),
    path('perfil/<int:perfil_id>/', exibir_perfil, name='exibir'),
    path('deletepostagem/<int:id_postagem>', delete_postagem, name='delete_postagem'),
]