# Generated by Django 4.0.1 on 2022-03-08 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('al_games', '0020_alter_ofertas_juegos_de_mesa_precio'),
    ]

    operations = [
        migrations.AddField(
            model_name='ofertas_juegos_de_mesa',
            name='enlaces_tiendas',
            field=models.URLField(default='https://aulangames.com/producto/zingo-bilingue/'),
            preserve_default=False,
        ),
    ]