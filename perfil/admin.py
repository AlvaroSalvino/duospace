from django.contrib import admin
from .models import *

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'fonte', 'cor', 'background', 'usuario', 'imagem_perfil', 'imagem_capa')
    search_fields = ('nome', 'telefone', 'usuario__email')
    list_filter = ('fonte', 'cor', 'background')
    readonly_fields = ('imagem_perfilURL', 'imagem_capaURL')
    filter_horizontal = ('contatos',)

class ConviteAdmin(admin.ModelAdmin):
    list_display = ('solicitante', 'convidado')
    search_fields = ('solicitante__user__username', 'convidado__user__username')
    list_filter = ('solicitante', 'convidado')

class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'perfil', 'data_postagem')
    search_fields = ('titulo', 'perfil__user__username')
    list_filter = ('data_postagem', 'perfil')
    
class CurtidaAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'post', 'data_curtida')
    search_fields = ('perfil__user__username', 'post__titulo')
    list_filter = ('data_curtida',)

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'post', 'texto', 'data_comentario')
    search_fields = ('perfil__user__username', 'post__titulo', 'texto')
    list_filter = ('data_comentario',)

admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Convite, ConviteAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Curtida, CurtidaAdmin)
admin.site.register(Comentario, ComentarioAdmin)
