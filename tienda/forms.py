from django import forms
from .models import Pedido

class FormularioCompra(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'nombre',
            'apellidos',
            'telefono',
            'email',
            'direccion',
            'suscripcion_boletin',
            'crear_cuenta',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tus apellidos'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+53 ...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tuemail@ejemplo.com'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dirección de envío'}),
            'suscripcion_boletin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'crear_cuenta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
            'direccion': 'Dirección',
            'suscripcion_boletin': 'Suscribirme al boletín',
            'crear_cuenta': 'Crear una cuenta',
        }
