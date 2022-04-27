diccionario_categorias = {'Familiares':5, 'Eurogame':1, 'Cooperativo':2, 'Para 2':4, 'Solitario':6, 'Fiesta':7, 'Experencia':9, 'Narrativo':10, 'Rápido':11, 'Infantil':12, 'Viaje':13, 'Ameritrash':14}


def categorias(pepe):
    for x in diccionario_categorias:
        valor = diccionario_categorias[x]
        if x == pepe:
            return valor
        else:
            valor = 8


