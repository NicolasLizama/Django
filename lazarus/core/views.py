#views.py
from django.shortcuts import render, redirect
from supabase import create_client, Client
from django.http import JsonResponse

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
                #uid = response.user.id
                data = {
                    #"uid": uid,
                    "nombre": nombre,
                    "apellido": apellido,
                    "email": email,
                    "fecha_nacimiento": fecha_nacimiento,
                    "telefono": telefono,
                    "rut": rut
                }
                supabase.table("usuarios").insert(data).execute()
            else:
                return redirect('/crear')
        except Exception as e:
            print(e)
            return redirect('/crear')
    return redirect('/')

#Proteccion de rutas por token supabase
def supabase_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        access_token = request.session.get("access_token")
        if not access_token:
            return render(request, 'ingreso.html')

        try:
            user = supabase.auth.get_user(access_token)
            if not user or not user.user:
                return render(request, 'ingreso.html')
        except Exception as e:
            print("Token inválido:", e)
            return render(request, 'ingreso.html')

        return view_func(request, *args, **kwargs)
    return wrapper


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
                request.session["access_token"] = session.session.access_token
                request.session["refresh_token"] = session.session.refresh_token
                request.session["nombre"] = session.user.user_metadata.get("nombre", email)
        except Exception as e:
            print(e)
            return redirect('/fail')
    return redirect('/oficial')

#proteccion de la pagina oficial si detecta token
@supabase_login_required
def oficial(request):
     nombre = request.session.get("nombre", "Usuario")
     return render(request, "oficial.html", {"nombre": nombre})



def recuperar_contraseña(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            supabase.auth.reset_password_for_email(email)
            message = "Se ha enviado un correo con las instrucciones para restablecer tu contraseña (revisa también la carpeta de SPAM)."
        except Exception as e:
            print("Error al enviar correo:", e)
            message = "El correo electrónico no está registrado o hubo un problema al enviar el correo. Verifica el correo e inténtalo nuevamente."

        return JsonResponse({'message': message})
    
    return render(request, 'recuperar_contraseña.html')


# Vista para cerrar sesión
def logout_view(request):
    request.session.flush()  # elimina toda la sesión de Django
    return redirect('/')


# # --- 1. Mostrar la página de cambio de contraseña ---
# def mostrarCambioPassword(request):
#     token = request.GET.get("access_token")  # token enviado por Supabase en el link

#     if not token:
#         # Si no hay token, redirige al inicio
#         return redirect('/')

#     # Si hay token, muestra la página cambioPass.html
#     return render(request, 'CambioPass.html', {"token": token})


# # --- 2. Procesar el cambio de contraseña ---
# def HacercambiarPassword(request):
#     if request.method == "POST":
#         token = request.POST.get("token")
#         nueva_contrasena = request.POST.get("password")

#         if not token or not nueva_contrasena:
#             return render(request, 'recuperar_contraseña.html', {
#                 "error": "Faltan datos para cambiar la contraseña."
#             })

#         try:
#             # Actualizar la contraseña en Supabase usando el token
#             supabase.auth.update_user({"password": nueva_contrasena}, access_token=token)
#             return render(request, 'recuperar_contraseña.html', {
#                 "success": "Contraseña cambiada correctamente. Ya puedes iniciar sesión."
#             })
#         except Exception as e:
#             print("Error al cambiar contraseña:", e)
#             return render(request, 'recuperar_contraseña.html', {
#                 "error": "No se pudo cambiar la contraseña. Intenta nuevamente."
#             })

#     # Si no es POST, vuelve al inicio
#     return redirect('/')


# Función para salir no funciona ahora
# def salir(request):
#     try:
#         del request.session['uid'] 
#     except KeyError:
#         pass
#     return redirect('/')