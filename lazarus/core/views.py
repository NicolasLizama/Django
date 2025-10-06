from django.shortcuts import render
from django.shortcuts import redirect
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
   };

firebase= pyrebase.initialize_app(config)
authe= firebase.auth()
database= firebase.database()

# Vistas paginas
def paginator(request):
    #wea= database.child('users').child('users').get().val()
    return render(request, 'ingreso.html')

def paginator2(request):
    return render(request, 'CrearUsuario.html')

def paginatorfail(request):
    return render(request, 'login.html')

# Creacion de funciones 

def usercreate(request):
    nombre = request.POST.get('nombre')
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authe.create_user_with_email_and_password(nombre,email,password)
    uid = user['localid']

    

    
    return render(request,"oficial.html")
    


def ingresar(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
      user = authe.sign_in_with_email_and_password(email,password)
    except:
       message ="ta malo con lo que existe"
       return render(request, "ingreso.html", {"correo": email})
    
    return render(request,"oficial.html")



def salir(request):
    try:
        del request.session['uid'] 
    except KeyError:
        pass
    return render(request,"ingreso.html")
