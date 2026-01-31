from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
        
class Curso(models.Model):
    """
    Modelo que representa un curso de ajedrez dentro de la plataforma.
    Incluye información básica, nivel, instructor, precio, duración y multimedia.
    """

    # Información principal
    titulo = models.CharField(max_length=200, unique=True, help_text="Título del curso")
    slug = models.SlugField(unique=True, blank=True, help_text="URL amigable generada automáticamente")
    descripcion = models.TextField(help_text="Descripción detallada del curso")

    # Clasificación del curso
    NIVEL_CHOICES = [
        ('Principiante', 'Principiante'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado'),
        ('Todos', 'Todos'),
    ]
    nivel = models.CharField(max_length=50, choices=NIVEL_CHOICES, default='Principiante')

    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE,
        related_name='cursos',
        help_text="Categoría a la que pertenece el curso"
    )

    # Datos adicionales
    instructor = models.CharField(max_length=100, help_text="Nombre del instructor")
    duracion = models.PositiveIntegerField(help_text="Duración en horas")
    precio = models.DecimalField(max_digits=8, decimal_places=2, help_text="Precio en USD, EURO, USDT")
    fecha_inicio = models.DateField(help_text="Fecha de inicio del curso")
    instructor = models.CharField(max_length=100, help_text="Nombre del instructor")
    
    # Multimedia
    imagen = models.ImageField(upload_to='cursos/', blank=True, null=True, help_text="Imagen representativa del curso")

    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return f"{self.titulo} ({self.nivel})"

    def save(self, *args, **kwargs):
        """
        Genera automáticamente el slug a partir del título si no existe.
        """
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    # Métodos auxiliares
    def get_absolute_url(self):
        """
        Devuelve la URL pública del curso para usar en plantillas y redirecciones.
        """
        return reverse('cursos:detalle_curso', kwargs={'slug': self.slug})

    def es_gratuito(self):
        """
        Indica si el curso es gratuito (precio = 0).
        """
        return self.precio == 0

    def duracion_en_dias(self):
        """
        Convierte la duración en horas a días aproximados (8 horas por día).
        """
        return round(self.duracion / 8)
