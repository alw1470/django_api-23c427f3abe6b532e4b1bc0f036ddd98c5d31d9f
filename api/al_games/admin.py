from msilib.schema import Media
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


from .models import Categorias, Juegos_de_mesa, Ofertas_juegos_de_mesa, MediaLibreria, Blog, CategoriasBlog


class CategoriasAdmin(admin.ModelAdmin):
    list_display = ('titulo_categoria', 'slug')
    model = Categorias
admin.site.register(Categorias, CategoriasAdmin)

class Ofertas_juegos_de_mesaInlineAdmin(admin.StackedInline):
    model = Ofertas_juegos_de_mesa


@admin.register(Juegos_de_mesa)
class Juegos_de_mesaAdmin_export(ImportExportModelAdmin):
    list_display = ('titulo_juegos_de_mesa','categorias')
    list_filter = ['categorias']
    search_fields = ['titulo_juegos_de_mesa']
    prepopulated_fields = {"slug": ("slug",)}
    inlines = [Ofertas_juegos_de_mesaInlineAdmin]
    pass


@admin.register(Ofertas_juegos_de_mesa)
class Ofertas_juegos_de_mesaAdmin_export(ImportExportModelAdmin):
    list_display =('juego_de_mesa','precio','tienda')
    search_fields = ['juego_de_mesa_id']
    


class Ofertas_juegos_de_mesaAdmin(admin.ModelAdmin):
    list_display =('juego_de_mesa','precio','tienda')
    model = Ofertas_juegos_de_mesa

@admin.register(MediaLibreria)
class MediaLibreriaAdmin(admin.ModelAdmin):
    list_diplay=('imagenes', 'titulo_imagen')
    model = MediaLibreria



@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=('titulo', 'slug')
    model = Blog



@admin.register(CategoriasBlog)
class CategoriasBlogAdmin(admin.ModelAdmin):
    list_display=('titulo_categoria_blog', 'slug')
    model = CategoriasBlog



# class Juegos_de_mesaAdmin(admin.ModelAdmin):
#     list_display = ('categorias','titulo_juegos_de_mesa')
# admin.site.register(Juegos_de_mesa, Juegos_de_mesaAdmin)
