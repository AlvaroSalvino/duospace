from django.contrib import admin
from .models import Perfil

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'fonte', 'cor', 'background', 'usuario', 'imagem_perfil', 'imagem_capa')
    search_fields = ('nome', 'telefone', 'usuario__email')
    list_filter = ('fonte', 'cor', 'background')
    readonly_fields = ('imagem_perfilURL', 'imagem_capaURL')
    filter_horizontal = ('contatos',)

admin.site.register(Perfil, PerfilAdmin)
