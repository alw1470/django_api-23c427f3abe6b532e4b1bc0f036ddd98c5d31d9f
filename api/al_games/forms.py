from django import forms
from .models import Juegos_de_mesa

class DuracionChoiceForm(forms.Form):

    DURACION_CHOICES = [
        (g, g) for g in Juegos_de_mesa.objects.values_list('duracion', flat=True).distinct()[0:8]
    ]

    # genre = forms.ChoiceField(choices=GENRE_CHOICES)

    duracion = forms.MultipleChoiceField(
        choices=DURACION_CHOICES,
        widget=forms.CheckboxSelectMultiple()
    )

    AUTORES_CHOICES = [
        (h, h) for h in Juegos_de_mesa.objects.values_list('autores', flat=True).distinct()[0:8]
    ]

    autores = forms.MultipleChoiceField(
        choices=AUTORES_CHOICES,
        widget=forms.CheckboxSelectMultiple()
    )