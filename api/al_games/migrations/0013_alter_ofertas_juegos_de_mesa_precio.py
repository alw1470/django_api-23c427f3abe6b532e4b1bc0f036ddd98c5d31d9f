# Generated by Django 4.0.1 on 2022-01-20 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('al_games', '0012_alter_categorias_titulo_categoria_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ofertas_juegos_de_mesa',
            name='precio',
            field=models.BooleanField(),
        ),
    ]