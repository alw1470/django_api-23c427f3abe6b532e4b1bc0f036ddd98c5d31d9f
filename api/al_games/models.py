from email.mime import image
from urllib import response
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
import requests
from io import BytesIO
from django.core import files
from django.utils.html import escape




class Categorias(models.Model):
    titulo_categoria = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=255, null =True, blank=False, unique=True)
    body = RichTextField(blank=False, null = False)
    
    # Funcion para devolver el titulo de la categoria en el panel de admin
    def __unicode__(self):
        return self.titulo_categoria
        
    def __str__(self):
        return self.titulo_categoria

    # Funcion para guardar de manera automatica el titulo como url
    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo_categoria)
        super(Categorias, self).save(*args, **kwargs)


class Juegos_de_mesa(models.Model):
    categorias = models.ForeignKey(Categorias, related_name="padre", on_delete=models.CASCADE)
    titulo_juegos_de_mesa = models.CharField(max_length=200)
    votacion = models.CharField(max_length=255, blank=True)
    body = RichTextField(blank=False, null=False)
    imagen_juegos_de_mesa = models.ImageField(upload_to="media", null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True)
    imagen_url =  models.URLField()
    publicacion = models.CharField(max_length=255)
    autores = models.CharField(max_length=255)
    duracion = models.CharField(max_length=255)
    titulo_seo = models.CharField(max_length=255)
    description_seo = models.CharField(max_length=155)
    


    def guardar_categoria_juego_de_mesa(self, *args, **kwargs):
        self.slug = slugify(self.titulo_juegos_de_mesa)
        super(Juegos_de_mesa, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.titulo_juegos_de_mesa



class Ofertas_juegos_de_mesa(models.Model):
    juego_de_mesa = models.ForeignKey(Juegos_de_mesa, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=5,decimal_places=2)
    tienda = models.CharField(max_length=255)
    enlaces_tiendas =  models.URLField()
    

class MediaLibreria(models.Model):
    imagenes = models.ImageField(upload_to="media", null=True, blank=True)
    titulo_imagen = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.titulo_imagen


class CategoriasBlog(models.Model):
    titulo_categoria_blog = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=255, null =True, blank=False, unique=True)
    body = RichTextField(blank=False, null = False)
    
    # Funcion para devolver el titulo de la categoria en el panel de admin
    def __unicode__(self):
        return self.titulo_categoria_blog
        
    def __str__(self):
        return self.titulo_categoria_blog

    # Funcion para guardar de manera automatica el titulo como url
    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo_categoria_blog)
        super(Categorias, self).save(*args, **kwargs)




class Blog(models.Model):
    categorias = models.ForeignKey(CategoriasBlog, related_name="padre", on_delete=models.CASCADE)
    title_seo = models.CharField(max_length=155)
    description_seo = models.CharField(max_length=155)
    titulo = models.CharField(max_length=255)
    imagen_blog = models.ImageField(upload_to="media", null=True, blank=True)
    cuerpo_articulo = RichTextField(blank=False, null = False)
    slug =  models.SlugField(max_length=255, null=True, blank=True, unique=True)
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)
        super(Blog, self).save(*args, **kwargs)
