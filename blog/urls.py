# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Página principal del blog: lista de entradas
    path('', views.post_list, name='lista'),

    # Detalle de una entrada por slug
    path('entrada/<slug:slug>/', views.post_detail, name='detalle'),

    # Filtrar por categoría
    path('categoria/<slug:slug>/', views.post_por_categoria, name='por_categoria'),

    # Filtrar por etiqueta
    path('etiqueta/<str:etiqueta>/', views.post_por_etiqueta, name='por_etiqueta'),

    # Archivo por año y mes (ej: /blog/archivo/2026/01/)
    path('archivo/<int:year>/<int:month>/', views.post_archivo, name='archivo'),

    # Búsqueda de entradas
    path('buscar/', views.post_buscar, name='buscar'),
]
