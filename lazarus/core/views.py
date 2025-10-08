#views.py
from django.shortcuts import render, redirect
import pyrebase 

config = {
     'apiKey': "AIzaSyDOK385X7jO5D_16i1EcjnIBpDwVOZhDwc",
     'authDomain': "lazarusdb-d37a9.firebaseapp.com",
     'projectId': "lazarusdb-d37a9",
     'storageBucket': "lazarusdb-d37a9.firebasestorage.app",
     'messagingSenderId': "245173338005",
     'appId': "1:245173338005:web:54ff73c8920d358558409c",
     'measurementId': "G-4STFMWRSQY",
     'databaseURL': ""
   }

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

# Vistas páginas
def paginator(request):
    return render(request, 'ingreso.html')

def paginator2(request):
    return render(request, 'CrearUsuario.html')

def paginatorfail(request):
    return render(request, 'login.html')

def introduccion(request):
    return render(request, 'introduccion.html')

# Función de creación de usuario
def usercreate(request):
    nombre = request.POST.get('nombre')
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = authe.create_user_with_email_and_password(email, password)
    except:
        return redirect('/crear')
    
    return redirect('/')

# Función para iniciar sesión
def ingresar(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        users = authe.sign_in_with_email_and_password(email, password)
    except:
        message = "Usuario o contraseña incorrectos"
        return redirect('/')
    
    return render(request, "oficial.html")

# Función para salir
def salir(request):
    try:
        del request.session['uid'] 
    except KeyError:
        pass
    return redirect('/')

from django.http import JsonResponse

def recuperar_contraseña(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            authe.send_password_reset_email(email)
            message = "Se ha enviado un correo con las instrucciones para restablecer tu contraseña (Si no lo ves debe estar en SPAM)."
        except Exception as e:
            message = "El correo electrónico no está registrado o hubo un problema al enviar el correo. Verifica el correo e inténtalo nuevamente."

        return JsonResponse({'message': message})
    
    return render(request, 'recuperar_contraseña.html')