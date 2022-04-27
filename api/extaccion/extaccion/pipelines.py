# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from al_games.models import Juegos_de_mesa, Categorias
import sqlite3
from scrapy.exceptions import DropItem

conexion = sqlite3.connect(
    'C:/Users/Alberto/Desktop/Workspace/django_api/api/db.sqlite3')
cursor = conexion.cursor()




class ExtaccionPipeline:
    def process_item(self, item, spider):
        if spider.name not in ['create', 'zaca', 'ficha']: 
            enlaces= item["enlaces_tiendas"]
            precio = item["precio"]
            if enlaces and precio is not None:
                pepe = f'SELECT enlaces_tiendas, precio FROM al_games_ofertas_juegos_de_mesa WHERE enlaces_tiendas = "{item["enlaces_tiendas"]}" AND precio = {item["precio"]}'
                cursor.execute(pepe)
                todo = cursor.fetchone()
                if todo is not None:
                    precio_comprobacion = todo[1]
                    enlace_comprobacion = todo[0]
                    print(precio_comprobacion)
                    print(enlace_comprobacion)                

                    print(enlaces)
                    if enlace_comprobacion == enlaces:
                        raise DropItem("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ESTA OFERTA YA EXISTE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    elif precio_comprobacion != precio:   
                        item.save()
                        return item
                else:
                    item.save()
                    return item
            
            else:
                item.save()
                return item
        item.save()
        return item 

                

        
        

