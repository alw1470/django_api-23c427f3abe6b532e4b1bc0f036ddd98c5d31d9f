from email.mime import image
import re
from gc import callbacks
from os import link
from urllib import request
from venv import create
import requests
from urllib.request import Request
import scrapy
from extaccion.items import Create_gameItem
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from al_games.models import Juegos_de_mesa, Ofertas_juegos_de_mesa, Categorias
import time
import wget

class MesaSpider(scrapy.Spider):
    name = 'create'
    allowed_domains = ['www.ludonauta.es']
    start_urls = ['https://www.ludonauta.es/juegos-mesas-tiendas/listar-por-tienda/espacio-de-juegos']
    BASE_URL = 'https://www.ludonauta.es'

    def parse(self, response):
        for l in range(1, 128):
            url = f"https://www.ludonauta.es/juegos-mesas-tiendas/listar-por-tienda/espacio-de-juegos/page:{l}"
            comprobacion = requests.get(url)
            print(url)
            link_page_url = response.urljoin(url)
            yield scrapy.Request(link_page_url, callback=self.parse_extractor)
            time.sleep(2)
            if comprobacion.status_code == 404:
                break



    def parse_extractor(self, response):
        item = Create_gameItem()
        # PRECIO
        precio_sucio = response.xpath('//span[@title="Precio"]/text()').extract()
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

        for x in precio:
             precio_create = x

        link_sucio = response.xpath('//h3/a/@href').extract()
        titulo_juego_de_mesa_creado = response.xpath('//h3/a/text()').extract()
        for x in titulo_juego_de_mesa_creado:
            titulo_2 = x

        imagen_sucia = response.xpath('//tbody//img/@src').extract()
        imagen_limpia = []

        for x in imagen_sucia:
            x = re.sub("72x72-","",x)
            t = "https://www.ludonauta.es"
            m = t+x
            imagen_limpia.append(m)
        

        
        # output_directory = 'C:/Users/Alberto/Desktop/Workspace/django_api/api/al_games/templates/media' 
        # for x in imagen_limpia:
        #     url = x
        #     filename = wget.download(url)
        
        for x in imagen_limpia:
            imagen_limpia = x

        slug = []
        for x in link_sucio:
            x = re.sub("/juegos-mesas/", "",x)
            print(x)
            slug.append(x)


        for x in slug:
            slug_limpia = x


        item['categorias'] = Categorias.objects.get(id=8)
        item['slug'] = slug_limpia
        item['titulo_juegos_de_mesa'] = titulo_2
        item['votacion'] = precio_create
        item['body'] = "Texto Generico"
        item['imagen_url'] = imagen_limpia
        yield item



