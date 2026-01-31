from django.urls import path
from . import views

app_name = 'tienda'

urlpatterns = [
    # Página principal de la tienda
    path('', views.home, name='home'),

    # Catálogo de productos (listado dinámico)
    path('listado/', views.listado_productos, name='listado'),

    # Detalle de producto individual
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle'),

    # Filtrar productos por categoría,

    # Búsqueda de productos
    path('buscar/', views.buscar_productos, name='buscar'),

    # Carrito de compras
    path('carrito/', views.carrito, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),

    # CRUD de productos (opcional, si manejas formularios propios además del admin)
    path('crear/', views.crear_producto, name='crear'),
    path('editar/<int:producto_id>/', views.editar_producto, name='editar'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar'),

    # Checkout y confirmación
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    path('confirmacion/<int:pedido_id>/', views.confirmacion, name='confirmacion'),
]
