from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
import csv

from .models import Categoria, Entrada


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'slug', 'activa')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('activa',)
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ('nombre',)
    list_per_page = 25
    fieldsets = (
        (_("Información"), {
            "fields": ("nombre", "descripcion", "slug", "activa")
        }),
    )


@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    # Columnas en la lista
    list_display = (
        'id', 'miniatura', 'titulo', 'categoria', 'autor',
        'publicado', 'fecha_publicacion', 'fecha_actualizacion'
    )

    # Campos editables directamente desde la lista
    list_editable = ('publicado',)

    # Búsqueda y filtros
    search_fields = ('titulo', 'contenido', 'etiquetas', 'resumen', 'meta_title', 'meta_description')
    list_filter = ('publicado', 'categoria', 'autor', 'fecha_publicacion')
    date_hierarchy = 'fecha_publicacion'
    ordering = ('-fecha_publicacion',)
    list_per_page = 30

    # Autocompletado y optimizaciones
    autocomplete_fields = ('categoria', 'autor')
    prepopulated_fields = {"slug": ("titulo",)}

    # Campos de solo lectura y organización del formulario
    readonly_fields = ('fecha_actualizacion', 'tiempo_lectura', 'miniatura')
    fieldsets = (
        (_("Contenido"), {
            "fields": ("titulo", "slug", "resumen", "contenido", "imagen_destacada", "miniatura")
        }),
        (_("Clasificación"), {
            "fields": ("categoria", "etiquetas")
        }),
        (_("Publicación"), {
            "fields": ("autor", "publicado", "fecha_publicacion", "fecha_actualizacion")
        }),
        (_("SEO"), {
            "classes": ("collapse",),
            "fields": ("meta_title", "meta_description")
        }),
    )

    # Acciones en lote
    actions = ['accion_publicar', 'accion_despublicar', 'accion_marcar_destacado',
               'accion_quitar_destacado', 'export_as_csv']

    # Evita N+1 queries en la lista
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('categoria', 'autor')

    # Miniatura para mostrar imagen destacada
    def miniatura(self, obj):
        if getattr(obj, 'imagen_destacada', None):
            return format_html('<img src="{}" style="width: 80px; height: auto; object-fit: cover; border-radius:4px;" />',
                               obj.imagen_destacada.url)
        return "-"
    miniatura.short_description = "Imagen"

    # Tiempo de lectura (método de modelo esperado)
    def tiempo_lectura(self, obj):
        try:
            return f"{obj.tiempo_lectura_min()} min"
        except Exception:
            return "-"
    tiempo_lectura.short_description = "Tiempo de lectura"

    # Asignar autor automáticamente si no existe (y el usuario es staff)
    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.autor:
            obj.autor = request.user
        super().save_model(request, obj, form, change)

    # Hacer autor solo editable por superusers
    def get_readonly_fields(self, request, obj=None):
        ro = list(self.readonly_fields)
        if not request.user.is_superuser:
            ro.append('autor')
        return ro

    # Acciones: publicar / despublicar
    def accion_publicar(self, request, queryset):
        updated = queryset.update(publicado=True)
        self.message_user(request, _("%d entradas marcadas como publicadas.") % updated)
    accion_publicar.short_description = "Marcar seleccionadas como publicadas"

    def accion_despublicar(self, request, queryset):
        updated = queryset.update(publicado=False)
        self.message_user(request, _("%d entradas despublicadas.") % updated)
    accion_despublicar.short_description = "Marcar seleccionadas como no publicadas"

    # Acciones: marcar/quitar destacado (si tu modelo tiene campo 'destacado')
    def accion_marcar_destacado(self, request, queryset):
        if hasattr(Entrada, 'destacado'):
            updated = queryset.update(destacado=True)
            self.message_user(request, _("%d entradas marcadas como destacadas.") % updated)
        else:
            self.message_user(request, _("El modelo Entrada no tiene el campo 'destacado'."), level='warning')
    accion_marcar_destacado.short_description = "Marcar seleccionadas como destacadas"

    def accion_quitar_destacado(self, request, queryset):
        if hasattr(Entrada, 'destacado'):
            updated = queryset.update(destacado=False)
            self.message_user(request, _("%d entradas quitadas de destacadas.") % updated)
        else:
            self.message_user(request, _("El modelo Entrada no tiene el campo 'destacado'."), level='warning')
    accion_quitar_destacado.short_description = "Quitar destacadas a las seleccionadas"

    # Exportar seleccionadas a CSV
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = ['id', 'titulo', 'slug', 'autor', 'categoria', 'publicado', 'fecha_publicacion']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=entradas_export.csv'
        writer = csv.writer(response)

        writer.writerow([meta.get_field(f).verbose_name.title() if hasattr(meta.get_field(f), 'verbose_name') else f for f in field_names])
        for obj in queryset.select_related('autor', 'categoria'):
            row = [
                getattr(obj, 'id'),
                getattr(obj, 'titulo'),
                getattr(obj, 'slug'),
                getattr(obj.autor, 'username', '') if getattr(obj, 'autor', None) else '',
                getattr(obj.categoria, 'nombre', '') if getattr(obj, 'categoria', None) else '',
                getattr(obj, 'publicado'),
                getattr(obj, 'fecha_publicacion'),
            ]
            writer.writerow(row)
        return response
    export_as_csv.short_description = "Exportar seleccionadas a CSV"

    # Mensaje de ayuda en búsqueda (opcional)
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['search_help_text'] = _("Busca por título, contenido o etiquetas.")
        return super().changelist_view(request, extra_context=extra_context)
