import os
from django.core.wsgi import get_wsgi_application

# 📌 Aquí definimos el entorno de ejecución
# En PythonAnywhere se usará 'production'
# En tu PC se quedará como 'development' por defecto
os.environ.setdefault('DJANGO_ENV', 'production')

# 📌 Indicamos el módulo de configuración principal
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 🚀 Aplicación WSGI
application = get_wsgi_application()
