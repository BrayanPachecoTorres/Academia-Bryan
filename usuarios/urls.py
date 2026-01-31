from django.urls import path
from .views import login_view, registro_view

app_name = 'usuarios'  # 🔥 Esto registra el namespace 'usuarios'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
]

