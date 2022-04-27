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


class MesaSpider(scrapy.Spider):
    name = 'ficha'
    allowed_domains = ['www.ludonauta.es']
    start_urls = ['https://www.ludonauta.es/juegos-mesas-tiendas/listar-por-tienda/tablerum']
    BASE_URL = 'https://www.ludonauta.es'

    def parse(self, response):
        for l in range(1, 128):
            url = f"https://www.ludonauta.es/juegos-mesas-tiendas/listar-por-tienda/tablerum/page:{l}"
            comprobacion = requests.get(url)
            print(url)
            link_page_url = response.urljoin(url)
            yield scrapy.Request(link_page_url, callback=self.intermedio)
            time.sleep(2)
            if comprobacion.status_code == 404:
                break

    def intermedio(self, response):
        enlaces_incompletos = response.xpath('//h3/a/@href').extract()
        for x in enlaces_incompletos:
            enlace = 'https://www.ludonauta.es' + x
            print(f'OEOEOEOEOEEOEOEOEOEOEOEOEO{enlace}')
            enlace_url = response.urljoin(enlace)
            comprobacion = requests.get(enlace)
            yield scrapy.Request(enlace_url, callback=self.parse_extractor)
            time.sleep(2)
            if comprobacion.status_code == 404:
                break




    def parse_extractor(self, response):
        item = Create_gameItem()

        ## Año de publicacion
        item['publicacion'] = response.xpath('//dd/p').extract()[0]
        #Autores
        autores_sucio = response.xpath('//dd/p/a/@title').extract()[0]
        autores_sucio = re.sub("Listar juegos de mesa de autor: «","",autores_sucio) 
        autores_sucio = re.sub("»","",autores_sucio)
        item['autores'] = autores_sucio
        
        #Categorias
        item['categorias'] = Categorias.objects.get(id=8)
        
        #Duracion
        duracion_sucio = response.xpath('//div[@class="widget navy-bg p-xs text-center m-t-xxs"]/div/div/text()').extract()[1]
        duracion_sucio = duracion_sucio.replace("\n","")
        duracion_sucio = duracion_sucio.replace("\t","")
        item['duracion'] = duracion_sucio

        #Precio
        precio_sucio = response.xpath('//span[@title="Mejor precio"]/text()').extract()
        precio_sucio_v2 = [st.strip() for st in precio_sucio]
        primer_elemento_precio_sucio_v2 = precio_sucio_v2[0]
        segundo_elemento = response.xpath('//span[@class="small"]/text()').extract()[0]
        segundo_elemento = segundo_elemento.replace("€","")
        precio = primer_elemento_precio_sucio_v2 + segundo_elemento

        item['votacion'] = precio
        
        #Slug
        link_sucio = response.url
        link_sucio = link_sucio.replace("https://www.ludonauta.es/juegos-mesas/","")
        item['slug'] = link_sucio

        #Titulo
        titulo_lista = response.xpath('//h2/text()').extract()
        for x in titulo_lista:
            titulo = x
        item['titulo_juegos_de_mesa'] = titulo 
        
        #Descripcion
        descripcion = response.xpath('//div[@id="descripcion"]').extract()
        for ele in descripcion:
            descripcion = re.sub("<.*?>|&.*?;|\\n|\\xa0","",ele)
        item['body'] = descripcion

        
        #Imagen
        imagen_sucia = response.xpath('//img/@src').extract()[2]
        imagen = 'https://www.ludonauta.es' + imagen_sucia
        item['imagen_url'] = imagen

        yield item



