from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse

from itertools import product
from re import template
from django.db.models import Max, Min
from django.shortcuts import get_object_or_404, render
from django.template import context
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView
from .models import Juegos_de_mesa, Categorias, Ofertas_juegos_de_mesa, Blog, CategoriasBlog
from .forms import DuracionChoiceForm


def base(request):
    productos = Juegos_de_mesa.objects.filter(categorias = 8).annotate(precio_bajo=Min('ofertas_juegos_de_mesa__precio'))[0:8]
    return render(request, 'index.html', {'productos':productos})



def juegos_de_mesa_view(request, categorias_slug, juegos_de_mesa_slug):
    producto = get_object_or_404(Juegos_de_mesa, categorias__slug= categorias_slug, slug= juegos_de_mesa_slug)
    ofertas = Ofertas_juegos_de_mesa.objects.filter(juego_de_mesa = producto.id)
    precio_bajo = Ofertas_juegos_de_mesa.objects.filter(juego_de_mesa = producto.id).aggregate(precio_bajo=Min('precio'))
    ficha = get_object_or_404(Categorias, slug=categorias_slug)
    return render(request, 'ficha-producto.html', {'producto':producto, 'ofertas':ofertas, 'ficha':ficha, 'precio_bajo':precio_bajo})


def categorias(request, categorias_slug):
    productos = Juegos_de_mesa.objects.filter(categorias__slug = categorias_slug).annotate(precio_bajo=Min('ofertas_juegos_de_mesa__precio'))
    ficha = get_object_or_404(Categorias, slug=categorias_slug)
    return render(request, 'categorias.html', {'ficha':ficha, 'productos':productos})


def is_valid_queryparam(param):
    return param != '' and param is not None

def is_invalid_queryparam(param):
    return 


def filter(request):
    qs = Juegos_de_mesa.objects.all()

    titulo = request.GET.get('titulo_juegos_de_mesa')
    print(titulo)
    
    duracion = request.GET.get('duracion')
    print(duracion)
    publicacion = request.GET.get('publicacion')
    print(publicacion)

    autores = request.GET.get('autores')
    print(autores)
    
    votacion = request.GET.get('votacion')

    


    if is_valid_queryparam(titulo):
        prueba_titulo = qs.filter(titulo_juegos_de_mesa__contains=titulo).exists()
        if prueba_titulo == True:
            qs = qs.filter(titulo_juegos_de_mesa__contains=titulo).annotate(precio_bajo=Min('ofertas_juegos_de_mesa__precio'))
        else:
            qs = Juegos_de_mesa.objects.all()[0:8]


    elif is_valid_queryparam(duracion):
        qs = qs.filter(duracion=duracion).annotate(precio_bajo=Min('ofertas_juegos_de_mesa__precio'))
    
  
    elif is_valid_queryparam(autores):
        qs = qs.filter(autores=autores).annotate(precio_bajo=Min('ofertas_juegos_de_mesa__precio'))

    elif is_valid_queryparam(publicacion):
        qs = qs.filter(publicacion=publicacion).annotate(precio_bajo=Min('ofertas_juegos_de_mesa__precio'))

    elif is_valid_queryparam(votacion):
        qs = qs.filter(votacion=votacion).annotate(precio_bajo=Min('ofertas_juegos_de_mesa__precio'))
 
    else:
        qs = Juegos_de_mesa.objects.all()[0:8]

    return qs



def resultado(request):
    qs = filter(request)
    context = {
        'queryset': qs,
        'categorias': Categorias.objects.all()
    }
    return render(request, "resultado_view.html", context)



# def bands(request):
#     bands = Juegos_de_mesa.objects.all()
#     data = []
#     for band in bands:
#         data.append({'titulo_juego_de_mesa':band.titulo_juegos_de_mesa, 'duracion':band.duracion, 'autores':band.autores, 'publicacion':band.publicacion})

#     return JsonResponse(data, safe=False)

def filtro(request):
    qs = filter(request)
    productos = Juegos_de_mesa.objects.filter(categorias = 8).annotate(precio_bajo=Min('ofertas_juegos_de_mesa__precio'))[0:8]
    context = {'productos':productos ,'queryset': qs}
    
    return render(request, 'buscador.html', context)



def blog(request):
    articulos = Blog.objects.all()
    context = {'articulos': articulos}
    return render(request, "blog.html", context )


def articulo_blog(request, articulos_slug):
    articulos = get_object_or_404(Blog, slug = articulos_slug)
    return render(request, 'articulos.html', {'articulos':articulos})
