from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Entrada, Categoria
from .forms import EntradaForm

# Helper para comprobar staff
def is_staff(user):
    return user.is_authenticated and user.is_staff

# -----------------------------
# Gestión (solo staff)
# -----------------------------

@login_required
@user_passes_test(is_staff)
def crear_entrada(request):
    """
    Crear una nueva entrada (solo staff/admin).
    Las entradas creadas desde aquí pueden publicarse o guardarse como borrador.
    """
    if request.method == 'POST':
        form = EntradaForm(request.POST, request.FILES)
        if form.is_valid():
            entrada = form.save(commit=False)
            entrada.autor = request.user
            # Si el staff marca 'publicado' en el formulario, se publicará; si no, quedará como borrador.
            entrada.save()
            messages.success(request, "Entrada guardada correctamente.")
            return redirect('blog:detalle', slug=entrada.slug)
    else:
        form = EntradaForm()
    categorias = Categoria.objects.filter(activa=True).order_by('nombre')
    recientes = Entrada.objects.recientes(5)
    return render(request, 'blog/crear_entrada.html', {
        'form': form,
        'categorias': categorias,
        'recientes': recientes,
    })

# -----------------------------
# Vistas públicas del blog
# -----------------------------

def post_list(request):
    """
    Lista general de entradas publicadas con paginación.
    """
    posts_qs = Entrada.objects.publicadas().select_related('autor', 'categoria')
    paginator = Paginator(posts_qs, 10)  # 10 entradas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categorias = Categoria.objects.filter(activa=True).order_by('nombre')
    recientes = Entrada.objects.recientes(5)

    return render(request, 'blog/listado.html', {
        'page_obj': page_obj,
        'categorias': categorias,
        'recientes': recientes,
    })


def post_detail(request, slug):
    """
    Detalle de una entrada.
    - Público: solo entradas publicadas.
    - Staff: puede ver preview añadiendo ?preview=1 (útil para revisar borradores).
    """
    preview = request.GET.get('preview') == '1' and request.user.is_authenticated and request.user.is_staff

    if preview:
        # Staff preview: no filtro por publicado
        post = get_object_or_404(Entrada.objects.select_related('autor', 'categoria'), slug=slug)
    else:
        # Público: solo entradas publicadas y con fecha_publicacion <= now
        post = get_object_or_404(Entrada.objects.select_related('autor', 'categoria'),
                                 slug=slug,
                                 publicado=True,
                                 fecha_publicacion__lte=timezone.now())

    # Incrementar visitas solo para entradas publicadas (evitar contar previews)
    if not preview and hasattr(post, 'visitas'):
        try:
            post.incrementar_visitas()
        except Exception:
            # No bloquear la vista por errores en el contador
            pass

    relacionados = Entrada.objects.publicadas().filter(
        categoria=post.categoria
    ).exclude(pk=post.pk)[:3]

    categorias = Categoria.objects.filter(activa=True).order_by('nombre')
    recientes = Entrada.objects.recientes(5)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'relacionados': relacionados,
        'categorias': categorias,
        'recientes': recientes,
        'preview': preview,
    })


# -----------------------------
# Filtros por categoría y etiqueta
# -----------------------------

def post_por_categoria(request, slug):
    """
    Lista de entradas filtradas por categoría (solo publicadas).
    """
    categoria = get_object_or_404(Categoria, slug=slug, activa=True)
    posts_qs = Entrada.objects.por_categoria(slug).select_related('autor', 'categoria')

    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    recientes = Entrada.objects.recientes(5)
    categorias = Categoria.objects.filter(activa=True).order_by('nombre')

    return render(request, 'blog/post_por_categoria.html', {
        'categoria': categoria,
        'page_obj': page_obj,
        'categorias': categorias,
        'recientes': recientes,
    })


def post_por_etiqueta(request, etiqueta):
    """
    Lista de entradas filtradas por etiqueta (solo publicadas).
    """
    posts_qs = Entrada.objects.publicadas().filter(etiquetas__icontains=etiqueta)

    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    recientes = Entrada.objects.recientes(5)
    categorias = Categoria.objects.filter(activa=True).order_by('nombre')

    return render(request, 'blog/post_por_etiqueta.html', {
        'etiqueta': etiqueta,
        'page_obj': page_obj,
        'categorias': categorias,
        'recientes': recientes,
    })


# -----------------------------
# Archivo por fecha
# -----------------------------

def post_archivo(request, year, month):
    """
    Lista de entradas publicadas en un año/mes específico.
    """
    posts_qs = Entrada.objects.publicadas().filter(
        fecha_publicacion__year=year,
        fecha_publicacion__month=month
    )

    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    recientes = Entrada.objects.recientes(5)
    categorias = Categoria.objects.filter(activa=True).order_by('nombre')

    return render(request, 'blog/post_archivo.html', {
        'page_obj': page_obj,
        'year': year,
        'month': month,
        'categorias': categorias,
        'recientes': recientes,
    })


# -----------------------------
# Búsqueda
# -----------------------------

def post_buscar(request):
    """
    Búsqueda de entradas por título, contenido o etiquetas (solo publicadas).
    """
    query = request.GET.get('q', '').strip()
    posts_qs = Entrada.objects.publicadas()

    if query:
        posts_qs = posts_qs.filter(
            Q(titulo__icontains=query) |
            Q(contenido__icontains=query) |
            Q(etiquetas__icontains=query)
        ).distinct()

    paginator = Paginator(posts_qs.order_by('-fecha_publicacion'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    recientes = Entrada.objects.recientes(5)
    categorias = Categoria.objects.filter(activa=True).order_by('nombre')

    return render(request, 'blog/post_buscar.html', {
        'query': query,
        'page_obj': page_obj,
        'categorias': categorias,
        'recientes': recientes,
    })


# -----------------------------
# Home (Inicio del sitio)
# -----------------------------

from cursos.models import Curso
from tienda.models import Producto
from django.contrib.auth.models import User

def home(request):
    """
    Página de inicio con contenido dinámico: cursos, últimas entradas publicadas,
    productos destacados y estadísticas.
    """
    cursos_destacados = Curso.objects.filter(destacado=True)[:3]
    posts_recientes = Entrada.objects.publicadas().order_by('-fecha_publicacion')[:3]
    productos_destacados = Producto.objects.filter(destacado=True)[:4]

    total_cursos = Curso.objects.count()
    total_posts = Entrada.objects.publicadas().count()
    total_usuarios = User.objects.count()

    year = datetime.now().year

    return render(request, 'home.html', {
        'cursos_destacados': cursos_destacados,
        'posts_recientes': posts_recientes,
        'productos_destacados': productos_destacados,
        'total_cursos': total_cursos,
        'total_posts': total_posts,
        'total_usuarios': total_usuarios,
        'testimonios': [],
        'year': year,
    })
