from import_export import resources
from .models import Juegos_de_mesa

class Juegos_de_mesaResource(resources.ModelResource):
    class Meta:
        model = Juegos_de_mesa