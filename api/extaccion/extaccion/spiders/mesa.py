from email.mime import image
from gc import callbacks
from os import link
from urllib import request
from venv import create
import requests
from urllib.request import Request
import scrapy
import sqlite3
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor, defer
from extaccion.items import CaballerosMesaItem, ZacatrusItem
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from al_games.models import Juegos_de_mesa, Ofertas_juegos_de_mesa, Categorias
import time

conexion = sqlite3.connect(
    'C:/Users/Alberto/Desktop/django_api-23c427f3abe6b532e4b1bc0f036ddd98c5d31d9f/api/db.sqlite3')
cursor = conexion.cursor()
cursor.execute("SELECT titulo_juegos_de_mesa, id FROM al_games_juegos_de_mesa")
todo = cursor.fetchall()


class MesaSpider(scrapy.Spider):
    name = 'mesa'
    allowed_domains = ['www.ludonauta.es']
    start_urls = [
        'https://www.ludonauta.es/juegos-mesas-tiendas/listar-por-tienda/cartoon-corp']
    BASE_URL = 'https://www.ludonauta.es'

    def parse(self, response):
        for l in range(1, 128):
            url = f"https://www.ludonauta.es/juegos-mesas-tiendas/listar-por-tienda/cartoon-corp/page:{l}"
            comprobacion = requests.get(url)
            print(url)
            link_page_url = response.urljoin(url)
            yield scrapy.Request(link_page_url, callback=self.parse_extractor)
            time.sleep(2)
            if comprobacion.status_code == 404:
                break


    def parse_extractor(self, response):
        item = CaballerosMesaItem()

        # PRECIO
        precio_sucio = response.xpath(
            '//span[@title="Precio"]/text()').extract()
        precio_sucio_v2 = [st.strip() for st in precio_sucio]
        a = [elemento for elemento in precio_sucio_v2 if elemento != '']
        p = response.xpath('//span[@class="small"]/text()').extract()
        lista_vacia = []
        for x in p:
            b = x.replace(",", ".")
            lista_vacia.append(b)

        diccionario_dos = []
        for x in lista_vacia:
            r = x.replace("€", "")
            diccionario_dos.append(r)

        i = 0
        precio = []
        for x in a:
            k = a[i] + diccionario_dos[i]
            h = float(k)
            i = i+1
            precio.append(h)

        titulo = response.xpath(
            '//h3[@class="m-t-xs m-b-xs"]/a/text()').extract()
            
        enlaces = response.xpath('//div[@class="pull-right"]/a/@href').extract()


        # Se crea un diccionario con las dos listas
        dict_from_list = dict(zip(titulo, precio))
        dicionario_enlaces = dict(zip(titulo, enlaces))
        #Enlaces para las ofertas de las tiendas.
        
        
            

        # for key, value in dict_from_list.items():
        # Nos sirve para recorrer un diccionario y sacar su key y su value

        for x in todo:
            titulo_prueba = x[0]
            valor = x[1]
            for key, value in dict_from_list.items():
                if titulo_prueba == key:
                    item['juego_de_mesa'] = Juegos_de_mesa.objects.get(
                        id=valor)
                    item['precio'] = value
                    item['tienda'] = 'Cartoon Corp'
                for key, value in dicionario_enlaces.items():
                    if titulo_prueba == key:
                        item['enlaces_tiendas'] = value

        yield item            



