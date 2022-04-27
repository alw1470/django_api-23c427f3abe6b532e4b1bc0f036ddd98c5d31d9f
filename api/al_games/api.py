from django.http import HttpResponse, HttpResponseNotFound
from typing import List
from ninja import NinjaAPI, ModelSchema
from django.db.models import Max, Min
from ninja.orm import create_schema
from django.http import JsonResponse


from .models import Juegos_de_mesa, Categorias, Ofertas_juegos_de_mesa

api = NinjaAPI(csrf=True)


Juegos_de_mesaSchema = create_schema(Juegos_de_mesa, depth=1)

# class BandSchema(ModelSchema):
#     class Config:
#         model = Juegos_de_mesa
#         model_fields = ['titulo_juegos_de_mesa', 'duracion', 'autores', 'imagen_url', 'publicacion', 'slug', 'votacion', 'categorias']

@api.get('bands', response=List[Juegos_de_mesaSchema])
def bands(request):
    return Juegos_de_mesa.objects.all()