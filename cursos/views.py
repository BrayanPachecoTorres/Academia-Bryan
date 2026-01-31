from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Curso

# Página principal de Cursos
def home(request: HttpRequest) -> HttpResponse:
    """
    Vista principal de la sección Cursos.
    Puede mostrar cursos destacados o información introductoria.
    """
    cursos_destacados = Curso.objects.order_by('-fecha_inicio')[:3]  # últimos 3 cursos
    context = {
        'cursos_destacados': cursos_destacados,
    }
    return render(request, 'cursos/home.html', context)


# Listado de cursos
def lista_cursos(request: HttpRequest) -> HttpResponse:
    """
    Muestra el listado completo de cursos disponibles.
    """
    cursos = Curso.objects.all()
    context = {
        'cursos': cursos,
    }
    return render(request, 'cursos/listado.html', context)


# Vista de detalle de un curso
def detalle_curso(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Muestra información detallada de un curso específico usando su slug.
    """
    curso = get_object_or_404(Curso, slug=slug)
    context = {
        'curso': curso,
    }
    return render(request, 'cursos/detalle.html', context)
