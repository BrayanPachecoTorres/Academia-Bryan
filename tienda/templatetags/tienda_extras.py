from django import template

register = template.Library()

# Obtener cantidad de un producto en el carrito
@register.filter
def get_item(carrito, producto_id):
    """
    Devuelve la cantidad de un producto en el carrito.
    Uso en plantilla: {{ carrito|get_item:producto.id }}
    """
    return carrito.get(str(producto_id), 0)


# Calcular subtotal de todos los productos en el carrito
@register.filter
def calc_subtotal(productos, carrito):
    """
    Devuelve el subtotal del carrito sumando precio * cantidad.
    Uso en plantilla: {{ productos|calc_subtotal:carrito }}
    """
    total = 0
    for producto in productos:
        cantidad = carrito.get(str(producto.id), 0)
        total += producto.precio * cantidad
    return total


# Multiplicar dos valores (ejemplo: precio × cantidad)
@register.filter
def mul(value, arg):
    """
    Multiplica dos valores numéricos.
    Uso en plantilla: {{ producto.precio|mul:carrito|get_item:producto.id }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
