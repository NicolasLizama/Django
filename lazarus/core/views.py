from django.shortcuts import render
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

# Create your views here.
def paginator(request):
    #wea= database.child('users').child('users').get().val()
    return render(request, 'pag.html')

def paginatorfail(request):
    return render(request, 'login.html')

def ingresar(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
      user = authe.sign_in_with_email_and_password(email,password)
    except:
       message ="ta malo con lo que existe"
       return render(request, "oficial.html", {"correo": email})
    
    return render(request,"oficial.html")


