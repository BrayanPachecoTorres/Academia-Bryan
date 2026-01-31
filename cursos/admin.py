from django.contrib import admin
from django.utils.html import format_html
from .models import Curso, Categoria   

# --- Registrar Categoría ---
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'slug', 'descripcion')   # columnas en listado
    search_fields = ('nombre','descripcion',)               # barra de búsqueda
    prepopulated_fields = {"slug": ("nombre",)}  # autocompletar slug

# --- Registrar Curso ---
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista de cursos
    list_display = (
        'id', 'titulo', 'nivel', 'instructor', 'precio',
        'duracion', 'fecha_inicio', 'categoria',  
        'imagen_preview', 'fecha_creacion'
    )
    list_filter = ('nivel', 'fecha_inicio', 'instructor', 'categoria')   
    search_fields = ('titulo', 'descripcion', 'instructor')
    ordering = ('-fecha_inicio',)
    list_per_page = 20
    date_hierarchy = 'fecha_inicio'
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'imagen_preview')

    # Organización de los campos en secciones
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'slug', 'descripcion', 'nivel', 'instructor', 'categoria',)  
        }),
        ('Detalles del curso', {
            'fields': ('precio', 'duracion', 'fecha_inicio')
        }),
        ('Multimedia', {
            'fields': ('imagen', 'imagen_preview')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    # Vista previa de la imagen en el admin
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-height: 150px; object-fit: contain;"/>',
                obj.imagen.url
            )
        return "(sin imagen)"
    imagen_preview.short_description = 'Vista previa'
