#views.py
from django.shortcuts import render, redirect
import pyrebase 
import firebase_admin
from firebase_admin import credentials, firestore

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

# --- Inicializa Pyrebase (para Auth) ---
firebase_client = pyrebase.initialize_app(config)
authe = firebase_client.auth()

# --- Inicializa Firebase Admin (para Firestore) --- cambiar a la ruta tuya personal
json_firebase = r"C:\Users\nicol\Desktop\proyect\lazarusdb-d37a9-firebase-adminsdk-fbsvc-2b55ec66c6.json"

# Solo inicializa una vez (evita error “already exists”)
if not firebase_admin._apps:
    cred = credentials.Certificate(json_firebase)
    firebase_admin.initialize_app(cred)

db = firestore.client()  # <- ahora funciona correctamente

# Vistas páginas
def paginator(request):
    return render(request, 'ingreso.html')

def paginator2(request):
    return render(request, 'CrearUsuario.html')

def paginatorfail(request):
    return render(request, 'login.html')

def introduccion(request):
    return render(request, 'introduccion.html')

def usercreate(request):
    nombre = request.POST.get('nombre')
    email = request.POST.get('email')
    apellido = request.POST.get('apellido')
    fecha_nacimiento = request.POST.get('fecha_nacimiento')
    telefono = request.POST.get('telefono')
    password = request.POST.get('password')
    
    try:
        user = authe.create_user_with_email_and_password(email,password)
        uid = user['localId']
        data = {
                'uid': uid,
                'nombre': nombre,
                'apellido': apellido,
                'email': email,
                'fecha_nacimiento': fecha_nacimiento,
                'telefono': telefono,
                
        }
        db.collection('users').document(uid).set(data)

    except:
        return redirect('/crear')
    # #lleva a la pagina url normal con nada     
    return redirect('/')


# Función para iniciar sesión
def ingresar(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
      user = authe.sign_in_with_email_and_password(email,password)
    except:
       message ="ñao ñao no existe"
       return redirect('/') 
    
    return render(request,"oficial.html")


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