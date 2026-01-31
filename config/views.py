from django.shortcuts import render
from cursos.models import Curso
from tienda.models import Producto
from blog.models import Entrada  # suponiendo que tu app blog tenga un modelo Entrada
# si tu app IA tiene un modelo, también lo puedes importar

def inicio(request):
    # 📚 Cursos destacados
    cursos_destacados = Curso.objects.all().order_by('-fecha_inicio')[:3]

    # 🛍️ Productos destacados
    productos_destacados = Producto.objects.all().order_by('-fecha_creacion')[:3]

    # 📰 Últimas entradas del blog
    entradas_blog = Entrada.objects.all().order_by('-fecha_publicacion')[:3]

    contexto = {
        'cursos_destacados': cursos_destacados,
        'productos_destacados': productos_destacados,
        'entradas_blog': entradas_blog,
    }

    return render(request, 'index.html', contexto)
