from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # importa la vista principal que tú creaste en config/views.py

urlpatterns = [
    # 🔑 Administración
    path('admin/', admin.site.urls),

    # 🌐 Página principal
    path('', views.inicio, name='inicio'),   # raíz del sitio → index.html

    # 📚 Apps del proyecto
    path('academia/', include('academia.urls')), # rutas de la app academia
    path('cursos/', include('cursos.urls')),     # rutas de la app cursos
    path('tienda/', include('tienda.urls')),     # rutas de la app tienda
    path('blog/', include('blog.urls')),         # rutas de la app blog
    path('usuarios/', include('usuarios.urls')), # rutas de la app usuarios
    path('ia/', include('ia.urls')),             # rutas de la app IA
]

# 📂 Configuración para servir archivos estáticos y multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
