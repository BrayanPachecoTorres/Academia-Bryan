from django.db import models

# Categorías de productos (ejemplo: Libros, Tableros, Accesorios)
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


# Modelo principal de Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    autor = models.CharField(max_length=100, blank=True, null=True)  # opcional, útil para libros
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name="productos")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre

    # Método auxiliar para saber si hay stock
    def disponible(self):
        return self.stock > 0


# 🧾 Modelo de Pedido (datos del cliente y resumen del pedido)
class Pedido(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    suscripcion_boletin = models.BooleanField(default=False)
    crear_cuenta = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.id} - {self.nombre} {self.apellidos}"


# 📦 Modelo de Línea de Pedido (productos dentro del pedido)
class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='lineas', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Línea de Pedido"
        verbose_name_plural = "Líneas de Pedido"

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} × {self.producto.nombre} (Pedido #{self.pedido.id})"
