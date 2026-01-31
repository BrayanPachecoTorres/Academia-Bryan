from django.contrib import admin
from django.utils.html import format_html
from .models import Producto, Categoria, Pedido, LineaPedido   # añadimos Pedido y LineaPedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')   # Mostrar ID para identificar duplicados
    search_fields = ('nombre', 'descripcion')        # Buscar por nombre y descripción
    ordering = ('nombre',)                           # Ordenar alfabéticamente
    list_per_page = 20                               # Paginación para no saturar la vista

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'nombre', 'precio', 'stock', 'categoria', 'fecha_creacion'
    )                                                # Mostrar ID y campos clave
    list_filter = ('categoria', 'fecha_creacion', 'stock')  # Filtros útiles
    search_fields = ('nombre', 'descripcion')        # Buscar por nombre y descripción
    ordering = ('nombre',)                           # Ordenar por nombre
    list_editable = ('precio', 'stock')              # Editar precio y stock directamente en la lista
    list_per_page = 20                               # Paginación
    date_hierarchy = 'fecha_creacion'                # Navegación por fechas
    readonly_fields = ('fecha_creacion',)            # No permitir modificar fecha de creación

    # Mantengo tu estructura original de fieldsets y añado la sección Multimedia
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'descripcion', 'categoria')
        }),
        ('Detalles de inventario', {
            'fields': ('precio', 'stock')
        }),
        ('Multimedia', {
            'fields': ('imagen', 'imagen_preview')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)  # Sección colapsable
        }),
    )

    # Agrego imagen_preview a readonly_fields para que se muestre en el formulario
    readonly_fields = ('fecha_creacion', 'imagen_preview')

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-height: 150px; object-fit: contain;"/>',
                obj.imagen.url
            )
        return "(sin imagen)"
    imagen_preview.short_description = 'Vista previa'


# 🧾 Administración de Pedidos y Líneas de Pedido
class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido
    extra = 0
    readonly_fields = ('subtotal',)

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = "Subtotal"


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellidos', 'email', 'telefono', 'fecha', 'total')
    search_fields = ('nombre', 'apellidos', 'email')
    list_filter = ('fecha', 'suscripcion_boletin', 'crear_cuenta')
    ordering = ('-fecha',)
    date_hierarchy = 'fecha'
    inlines = [LineaPedidoInline]
    readonly_fields = ('fecha', 'total')

    fieldsets = (
        ('Datos del cliente', {
            'fields': ('nombre', 'apellidos', 'telefono', 'email', 'direccion')
        }),
        ('Opciones', {
            'fields': ('suscripcion_boletin', 'crear_cuenta')
        }),
        ('Resumen', {
            'fields': ('fecha', 'total')
        }),
    )


@admin.register(LineaPedido)
class LineaPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    search_fields = ('producto__nombre', 'pedido__nombre')
    list_filter = ('pedido',)
    ordering = ('pedido',)

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = "Subtotal"
