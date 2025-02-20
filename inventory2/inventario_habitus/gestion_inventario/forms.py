from django import forms
from .models import SolicitudTraslado, Almacen

class SolicitudTrasladoForm(forms.ModelForm):
    class Meta:
        model = SolicitudTraslado
        fields = ['almacen_destino', 'cantidad']
        widgets = {
            'almacen_destino': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }