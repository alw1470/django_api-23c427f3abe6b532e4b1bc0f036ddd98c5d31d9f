# Generated by Django 4.0.1 on 2022-01-12 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('al_games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='juegos_de_mesa',
            name='imagen_juegos_de_mesa',
            field=models.ImageField(null=True, upload_to='media'),
        ),
    ]
