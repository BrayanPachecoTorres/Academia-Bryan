from django.urls import path
from . import views

app_name = 'cursos'  # namespace para evitar conflictos con otras apps

urlpatterns = [
    # Página principal de cursos (home destacado)
    path('home/', views.home, name='home'),

    # Página raíz de cursos (puede mostrar listado o destacados)
    path('', views.lista_cursos, name='lista_cursos'),

    # Listado completo de cursos
    path('listado/', views.lista_cursos, name='listado_cursos'),

    # Detalle de curso usando slug (URL amigable)
    path('<slug:slug>/', views.detalle_curso, name='detalle_curso'),
]
