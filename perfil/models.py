from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import pillow_heif
import os


class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=15, null= False)
    imagem_perfil = models.ImageField(null=True, blank=True, upload_to='fotoPerfil/')
    imagem_capa = models.ImageField(null=True, blank=True, upload_to='fotocapa/')
    fonte = models.CharField(max_length=10, default='fonte-3')
    cor = models.CharField(max_length=10, default='cor-1')
    background = models.CharField(max_length=10, default='light')
    contatos = models.ManyToManyField('self')

    usuario = models.OneToOneField(User, related_name='perfil', on_delete=models.CASCADE)

    @property
    def email(self):
        return self.usuario.email

    def convidar(self, perfil_convidado):
        convite = Convite(solicitante=self,convidado = perfil_convidado)
        convite.save()

    def desfazer_amizade(self, perfil_amizade):
        self.contatos.remove(perfil_amizade.id)

    @property
    def imagem_perfilURL(self):
        try:
            url = self.imagem_perfil.url
        except:
            url = ''
        return url
    
    @property
    def imagem_capaURL(self):
        try:
            url = self.imagem_capa.url
        except:
            url = ''
        return url
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.imagem_perfil:
            img_path = self.imagem_perfil.path
            if img_path.lower().endswith(".heic"):
                heif_image = pillow_heif.open_heif(img_path)
                img = Image.frombytes(heif_image.mode, heif_image.size, heif_image.data)
                
                # Converter para .jpg
                new_path = os.path.splitext(img_path)[0] + ".jpg"
                img.save(new_path, format="JPEG")

                # Atualizar o campo imagem_perfil
                self.imagem_perfil.name = os.path.basename(new_path)
                self.save()  # Salvar novamente para atualizar o caminho da imagem

                # Remover a imagem .heic original
                os.remove(img_path)

class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil,on_delete=models.CASCADE,related_name='convites_feitos' )
    convidado = models.ForeignKey(Perfil, on_delete= models.CASCADE, related_name='convites_recebidos')

    def aceitar(self):
        self.convidado.contatos.add(self.solicitante)
        self.solicitante.contatos.add(self.convidado)
        self.delete()

    def rejeitar(self):
        self.delete()

class Post(models.Model):
    titulo = models.CharField(max_length=250)
    text = models.TextField()
    data_postagem = models.DateTimeField(auto_now=True)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='posts')
    imagem = models.ImageField(null=True, blank=True, upload_to='postagem/')

    @property
    def imagemURL(self):
        try:
            url = self.imagem.url
        except:
            url = ''
        return url
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.imagem:
            img_path = self.imagem.path
            if img_path.lower().endswith(".heic"):
                heif_image = pillow_heif.open_heif(img_path)
                img = Image.frombytes(heif_image.mode, heif_image.size, heif_image.data)
                
                # Converter para .jpg
                new_path = os.path.splitext(img_path)[0] + ".jpg"
                img.save(new_path, format="JPEG")

                # Atualizar o campo imagem
                self.imagem.name = os.path.basename(new_path)
                self.save()  # Salvar novamente para atualizar o caminho da imagem

                # Remover a imagem .heic original
                os.remove(img_path)