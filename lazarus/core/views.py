#views.py
from django.shortcuts import render, redirect
from supabase import create_client, Client


# Conectarse a la api de supabase 
url = "https://cixtrfcwsweaxtliwdgc.supabase.co"
# la key se conecta a la legacy api keys usando la PUBLIC ANON KEY 
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpeHRyZmN3c3dlYXh0bGl3ZGdjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAxMTA2MjUsImV4cCI6MjA3NTY4NjYyNX0.5hGTCUa9t7jghSE5hW-o-2vBPDTmyYZu7OzZwHgj0uA"  

supabase: Client = create_client(url, key)

#ideal lo mejor es guardar eso en un env. pero lo dejo despues para farmear mas commits







# Vistas páginas
def paginator(request):
    return render(request, 'ingreso.html')

def paginator2(request):
    return render(request, 'CrearUsuario.html')

def paginatorfail(request):
    return render(request, 'fail.html')

def introduccion(request):
    return render(request, 'introduccion.html')

def usercreate(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        rut = request.POST.get('rut')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        telefono = request.POST.get('telefono')
        password = request.POST.get('password')

        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            if response.user:
                uid = response.user.id
                data = {
                    "uid": uid,
                    "nombre": nombre,
                    "apellido": apellido,
                    "email": email,
                    "fecha_nacimiento": fecha_nacimiento,
                    "telefono": telefono,
                    "rut": rut
                }
                supabase.table("users").insert(data).execute()
            else:
                return redirect('/crear')
        except Exception as e:
            print(e)
            return redirect('/crear')
    return redirect('/')



def ingresar(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            session = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if session.user:
                request.session["supabase_user"] = session.user.id
        except Exception as e:
            print(e)
            return redirect('/fail')
    return render(request, "oficial.html")

# Función para salir no funciona ahora
def salir(request):
    try:
        del request.session['uid'] 
    except KeyError:
        pass
    return redirect('/')

from django.http import JsonResponse

# def recuperar_contraseña(request):
#     if request.method == "POST":
#         # email = request.POST.get('email')

#         # try:
#         #     authe.send_password_reset_email(email)
#         #     message = "Se ha enviado un correo con las instrucciones para restablecer tu contraseña (Si no lo ves debe estar en SPAM)."
#         # except Exception as e:
#         #     message = "El correo electrónico no está registrado o hubo un problema al enviar el correo. Verifica el correo e inténtalo nuevamente."

#         # return JsonResponse({'message': message})
    
#     return render(request, 'recuperar_contraseña.html')