# blog/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .models import Entrada, Categoria

class EntradaForm(forms.ModelForm):
    """
    Formulario para crear/editar entradas del blog.
    - Valida que el slug sea único (ignorando la propia instancia al editar).
    - Proporciona widgets y placeholders para mejor UX.
    """
    class Meta:
        model = Entrada
        fields = [
            'titulo',
            'slug',
            'categoria',
            'contenido',
            'resumen',
            'etiquetas',
            'imagen_destacada',  # nombre correcto del campo
            'publicado',
            'fecha_publicacion',
            'destacado',         # opcional, si lo expones en el formulario
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la entrada'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'slug-para-la-entrada (sin espacios)'
            }),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Escribe el contenido aquí...'
            }),
            'resumen': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Resumen breve (opcional)'
            }),
            'etiquetas': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'etiqueta1, etiqueta2, etiqueta3'
            }),
            'imagen_destacada': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'fecha_publicacion': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'publicado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'destacado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['categoria'].queryset = Categoria.objects.filter(activa=True).order_by('nombre')
        except Exception:
            pass

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        titulo = self.cleaned_data.get('titulo')

        if not slug and titulo:
            slug = slugify(titulo)

        if not slug:
            raise ValidationError('El slug no puede estar vacío.')

        qs = Entrada.objects.filter(slug=slug)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError('Ya existe una entrada con ese slug. Usa otro.')

        return slug

    def clean_imagen_destacada(self):
        """
        Validación simple de la imagen destacada (opcional).
        - Tamaño máximo 5MB
        - Tipos permitidos: jpeg, png, gif
        """
        imagen = self.cleaned_data.get('imagen_destacada')
        if imagen:
            max_mb = 5
            if imagen.size > max_mb * 1024 * 1024:
                raise ValidationError(f'La imagen no puede superar {max_mb} MB.')
            valid_content_types = ['image/jpeg', 'image/png', 'image/gif']
            content_type = getattr(imagen, 'content_type', None)
            if content_type and content_type not in valid_content_types:
                raise ValidationError('Formato de imagen no soportado. Usa JPEG, PNG o GIF.')
        return imagen
