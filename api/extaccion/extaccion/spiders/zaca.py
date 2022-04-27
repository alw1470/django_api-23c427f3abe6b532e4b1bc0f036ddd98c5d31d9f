from urllib.request import Request
import scrapy
from . import scripts
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor, defer
from extaccion.items import ZacatrusItem

from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from al_games.models import Juegos_de_mesa, Categorias
import requests
import tempfile
from django.core import files

class ZacaSpider(scrapy.Spider):
    name = 'zaca'
    allowed_domains = ['zacatrus.es']
    start_urls = ['https://zacatrus.es/catalogsearch/result/?q=juegos+de+mesa&amnoroute']

    def parse(self, response):
        enlaces =['https://zacatrus.es/juegos-de-mesa/familiares.html',
                'https://zacatrus.es/juegos-de-mesa/cooperativo.html',
                'https://zacatrus.es/juegos-de-mesa/solitario.html',
                'https://zacatrus.es/juegos-de-mesa/para_2.html',
                'https://zacatrus.es/juegos-de-mesa/experiencia.html',
                'https://zacatrus.es/juegos-de-mesa/fiesta.html',
                'https://zacatrus.es/juegos-de-mesa/narrativo.html',
                'https://zacatrus.es/juegos-de-mesa/rapido.html',
                'https://zacatrus.es/juegos-de-mesa/infantil.html',
                'https://zacatrus.es/juegos-de-mesa/viaje.html',
                'https://zacatrus.es/juegos-de-mesa/eurogame.html',
                'https://zacatrus.es/juegos-de-mesa/ameritrash.html']
        for enlace in enlaces:
            url = response.urljoin(enlace)
            yield scrapy.Request(url, callback = self.parse_categorias)
        
       
    def parse_categorias(self, response):
        links = response.xpath('//a[@class="product-item-link"]/@href').extract()
        for link in links:
            url_link = response.urljoin(link)
            yield scrapy.Request(url_link,  callback= self.paparse_extractor)
        
        next_page = response.xpath('//a[@title="Siguiente"]/@href').extract()
        for y in next_page:
            next_page_url = response.urljoin(y)
            yield scrapy.Request(next_page_url, self.parse_categorias)
    
    def paparse_extractor(self, response):
        item =  ZacatrusItem()
        
        #CATEGORIAS
        
        y = response.xpath('//td[@class="col data"]//text()').extract()[4]
        categoria = y.split()[0]
        categoria_limpia = categoria.replace(",","")
        valor = scripts.categorias(categoria_limpia)
        item['categorias']= Categorias.objects.get(id=valor)

        #SLUG
        link_sucio = response.url
        link_limpio = link_sucio.replace("https://zacatrus.es/","")
        link_relimpio = link_limpio.replace(".html","")
        slug = link_relimpio
        item['slug'] = slug
        
        #TITULO
        item['titulo_juegos_de_mesa'] = response.xpath('//h1/span[@itemprop ="name"]/text()').extract()[0]
        precio = response.xpath('//span[@class="price"]/text()').extract()[0]
        
        #PRECIO
        item['votacion'] = precio
        #item['categoria_id'] = 1

        #TEXTO
        item['body'] = response.xpath('//div[@class="value"]').extract()
        
        #IMAGEN
        image_url = response.xpath('//span[@class="thumbnail_url"]/text()').extract_first()
        item['imagen_url'] = image_url
        response = requests.get(image_url, stream=True)
        file_name = image_url
        lf = tempfile.NamedTemporaryFile()
        for block in response.iter_content(1024 * 8):
            if not block:
                break
            lf.write(block)
        item['imagen_juegos_de_mesa'] = (file_name, files.File(lf))