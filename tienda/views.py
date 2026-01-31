from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Producto, Categoria, Pedido, LineaPedido
from .forms import FormularioCompra

# -----------------------------
# Página principal de la Tienda
# -----------------------------
def home(request):
    destacados = Producto.objects.order_by('-fecha_creacion')[:4]
    categorias = Categoria.objects.all()
    return render(request, 'tienda/home.html', {
        'destacados': destacados,
        'categorias': categorias
    })

# -----------------------------
# Listado completo de productos
# -----------------------------
def listado_productos(request):
    productos = Producto.objects.all().order_by('nombre')
    categorias = Categoria.objects.all()

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    return render(request, 'tienda/listado.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_id
    })

# -----------------------------
# Vista de detalle de un producto
# -----------------------------
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    relacionados = Producto.objects.filter(
        categoria=producto.categoria
    ).exclude(id=producto.id)[:3]

    return render(request, 'tienda/detalle.html', {
        'producto': producto,
        'relacionados': relacionados
    })

# -----------------------------
# Búsqueda de productos
# -----------------------------
def buscar_productos(request):
    query = request.GET.get('q')
    productos = []
    if query:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        ).distinct()
    return render(request, 'tienda/buscar.html', {
        'query': query,
        'productos': productos,
    })

# -----------------------------
# Carrito de compras (simple con sesión)
# -----------------------------
def carrito(request):
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())
    return render(request, 'tienda/carrito.html', {
        'productos': productos,
        'carrito': carrito,
    })

def agregar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1
    request.session['carrito'] = carrito
    return redirect('tienda:carrito')

def eliminar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    carrito.pop(str(producto_id), None)
    request.session['carrito'] = carrito
    return redirect('tienda:carrito')

def vaciar_carrito(request):
    request.session['carrito'] = {}
    return redirect('tienda:carrito')

# -----------------------------
# Checkout (Finalizar compra)
# -----------------------------
def finalizar_compra(request):
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())

    if request.method == 'POST':
        form = FormularioCompra(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.total = 0
            pedido.save()

            # Crear líneas de pedido
            for producto in productos:
                cantidad = carrito[str(producto.id)]
                linea = LineaPedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )
                pedido.total += linea.subtotal()

            pedido.save()
            request.session['carrito'] = {}  # vaciar carrito

            return redirect('tienda:confirmacion', pedido_id=pedido.id)
    else:
        form = FormularioCompra()

    return render(request, 'tienda/checkout.html', {
        'form': form,
        'productos': productos,
        'carrito': carrito,
    })

# -----------------------------
# Confirmación de pedido
# -----------------------------
def confirmacion(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'tienda/confirmacion.html', {
        'pedido': pedido
    })

# -----------------------------
# CRUD de productos (opcional)
# -----------------------------
def crear_producto(request):
    return render(request, 'tienda/crear.html')

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'tienda/editar.html', {'producto': producto})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('tienda:listado')
