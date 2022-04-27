import sqlite3


conexion = sqlite3.connect(
    'C:/Users/Alberto/Desktop/Workspace/django_api/api/db.sqlite3')
cursor = conexion.cursor()

k = 14.95
l = "4833"
m = 'Crash Comics'
p = 'https://aulangames.com/producto/zingo-bilingue/'

sql=f'SELECT precio, tienda, juego_de_mesa_id, enlaces_tiendas FROM al_games_ofertas_juegos_de_mesa WHERE precio = {k} AND juego_de_mesa_id = {l}'
#pepe = f'SELECT precio, tienda, juego_de_mesa_id FROM al_games_ofertas_juegos_de_mesa WHERE tienda = "{m}" AND juego_de_mesa_id = {l}'

pepe = f'SELECT enlaces_tiendas, precio FROM al_games_ofertas_juegos_de_mesa WHERE enlaces_tiendas = "{p}" AND precio = {k}'
cursor.execute(pepe)
todo = cursor.fetchone()

jose = todo[1]


pepe = todo[0]
print(pepe)


print(jose)

u = ('Crash Comics', 4833)

print(todo)

if todo == u:
    print('hola')