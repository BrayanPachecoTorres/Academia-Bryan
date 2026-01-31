from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils import timezone


def unique_slugify(instance, value, slug_field_name="slug"):
    """
    Genera un slug único basado en 'value'.
    Si existe, añade sufijos -2, -3, ...
    """
    base_slug = slugify(value)[:50]  # límite razonable
    slug = base_slug
    ModelClass = instance.__class__
    n = 2
    while ModelClass.objects.filter(**{slug_field_name: slug}).exclude(pk=instance.pk).exists():
        slug = f"{base_slug}-{n}"
        n += 1
    return slug


class Categoria(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre de la categoría",
        validators=[MinLengthValidator(2)]
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        verbose_name="Slug"
    )
    activa = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.nombre)
        super().save(*args, **kwargs)


class EntradaQuerySet(models.QuerySet):
    def publicadas(self):
        return self.filter(publicado=True, fecha_publicacion__lte=timezone.now())

    def por_categoria(self, categoria_slug):
        return self.publicadas().filter(categoria__slug=categoria_slug)

    def recientes(self, limite=5):
        return self.publicadas().order_by('-fecha_publicacion')[:limite]


class Entrada(models.Model):
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título",
        validators=[MinLengthValidator(4)]
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        verbose_name="Slug"
    )
    resumen = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Resumen (opcional)",
        help_text="Si lo dejas vacío, se generará automáticamente a partir del contenido."
    )
    contenido = models.TextField(verbose_name="Contenido")
    autor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Autor"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        related_name="entradas",
        verbose_name="Categoría"
    )
    etiquetas = models.CharField(
        max_length=200,
        blank=True,
        help_text="Separar con comas",
        verbose_name="Etiquetas"
    )
    imagen_destacada = models.ImageField(
        upload_to='blog/',
        blank=True,
        null=True,
        verbose_name="Imagen destacada"
    )

    # Nuevos campos añadidos para compatibilidad con admin
    destacado = models.BooleanField(
        default=False,
        verbose_name="Destacado",
        help_text="Marcar para mostrar en secciones destacadas"
    )
    visitas = models.PositiveIntegerField(
        default=0,
        verbose_name="Visitas",
        help_text="Contador de visitas (incrementar desde la vista)"
    )

    publicado = models.BooleanField(
        default=True,
        verbose_name="Publicado"
    )
    fecha_publicacion = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de publicación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    # SEO opcional
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        verbose_name="Meta title"
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="Meta description"
    )

    objects = EntradaQuerySet.as_manager()

    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"
        ordering = ['-fecha_publicacion']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['publicado', 'fecha_publicacion']),
            models.Index(fields=['destacado']),
            models.Index(fields=['visitas']),
        ]

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        # Slug único
        if not self.slug:
            self.slug = unique_slugify(self, self.titulo)
        # Resumen automático si está vacío
        if not self.resumen:
            self.resumen = (self.contenido.strip().replace("\n", " ")[:297] + '...') if len(self.contenido) > 300 else self.contenido
        # Meta por defecto si está vacío
        if not self.meta_title:
            self.meta_title = self.titulo[:60]
        if not self.meta_description:
            base = self.resumen or self.contenido
            self.meta_description = base[:160]
        super().save(*args, **kwargs)

    def etiquetas_lista(self):
        return [et.strip() for et in self.etiquetas.split(",") if et.strip()]

    def tiempo_lectura_min(self):
        """
        Estimación simple: ~200 palabras/minuto.
        """
        palabras = len(self.contenido.split())
        minutos = max(1, round(palabras / 200))
        return minutos

    def incrementar_visitas(self, save=True):
        """
        Incrementa el contador de visitas. Llamar desde la vista cuando se muestre la entrada.
        """
        self.visitas = (self.visitas or 0) + 1
        if save:
            self.save(update_fields=['visitas'])
        return self.visitas

    def miniatura_url(self):
        """
        Devuelve la URL de la imagen destacada o None si no existe.
        Útil para el admin o para plantillas.
        """
        try:
            return self.imagen_destacada.url if self.imagen_destacada else None
        except Exception:
            return None
