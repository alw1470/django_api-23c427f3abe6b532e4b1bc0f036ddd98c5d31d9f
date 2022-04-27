# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from al_games.models import Juegos_de_mesa, Ofertas_juegos_de_mesa



class ZacatrusItem(DjangoItem):
    django_model = Juegos_de_mesa


class CaballerosMesaItem(DjangoItem):
    django_model = Ofertas_juegos_de_mesa


class Create_gameItem(DjangoItem):
    django_model = Juegos_de_mesa

