from django import views
from django.urls import path
from django.urls.conf import re_path
from .views import juegos_de_mesa_view
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .api import api 
 

urlpatterns =[
 path('<slug:categorias_slug>/', views.categorias, name='categorias'),
 path('<slug:categorias_slug>/<slug:juegos_de_mesa_slug>/', views.juegos_de_mesa_view, name='productos'),
 path('resultado', views.resultado, name='resultado'),
 path('buscador', views.filtro, name='buscador'),
 path('blog', views.blog, name="blog" ),
 path('<slug:articulos_slug>', views.articulo_blog, name='articulos_blog'),
 path('api/', api.urls)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
