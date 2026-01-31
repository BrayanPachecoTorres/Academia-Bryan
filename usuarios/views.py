from django.shortcuts import render

# Vista para el login
def login_view(request):
    return render(request, 'usuarios/login.html')

# Vista para el registro
def registro_view(request):
    return render(request, 'usuarios/registro.html')
