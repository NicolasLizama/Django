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
                "password": password,
                "options": {
                    "data": {
                        "nombre": nombre,
                        "apellido": apellido
                    }
                }
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
                request.session["nombre"] = session.user.user_metadata.get("nombre", session.user.email)
                request.session["email"] = session.user.email
        except Exception as e:
            print(e)
            return redirect('/fail')
    return redirect('/oficial')

#proteccion de la pagina oficial si detecta token
@supabase_login_required
def oficial(request):
    nombre = request.session.get("nombre", "Usuario")
    return render(request, "oficial.html", {"nombre": nombre})

@supabase_login_required
def gad7(request):
    return render(request, 'gad_7.html')

@supabase_login_required
def phq9(request):
    return render(request, 'phq9.html')

@supabase_login_required
def Test_reconocimiento(request):
    return render(request, 'Test_reconocimiento.html')


@supabase_login_required
def TestRecco_enviar(request):

    if request.method == "POST":
        # Obtener los datos del formulario
        carrera = request.POST.get('carrera')
        motivo_estudio = request.POST.get('motivo_estudio')
        año_estudio = request.POST.get('año_estudio')
        intereses = request.POST.get('intereses')
        malestar = request.POST.get('malestar')
        expect_inicial = request.POST.get('expect_inicial')
        razon = request.POST.get('razon')

        # Obtener el email del usuario actual desde la sesión
        email_usuario = request.session.get("email") or request.session.get("nombre")

        if not email_usuario:
            print("No se encontró el correo del usuario en la sesión.")
            return redirect('/fail')

        try:
            #  Buscar id_usuario en la tabla usuarios
            usuario_query = supabase.table("usuarios").select("id_usuario").eq("email", email_usuario).execute()

            if not usuario_query.data:
                print(f"No se encontró el usuario con correo {email_usuario} en la tabla usuarios.")
                return redirect('/fail')

            id_usuario = usuario_query.data[0]["id_usuario"]

            # Preparar datos para insertar en Test_reconocimiento
            data = {
                "id_usuario": id_usuario,
                "carrera": carrera,
                "motivo_estudio": motivo_estudio,
                "año_estudio": año_estudio,
                "intereses": intereses,
                "malestar": malestar,
                "expect_inicial": expect_inicial,
                "razon": razon
            }

            # Preparar datos para insertar en carrera
            data_carrera = {
                "id_usuario": id_usuario,
                "nombre_carrera": carrera
            }   

            # Insertar en tabla Test_reconocimiento
            supabase.table("Test_reconocimiento").insert(data).execute()

            # Insertar en tabla en carrera
            supabase.table("carrera").insert(data_carrera).execute()

            print(f"✅ Test de reconocimiento guardado para usuario {email_usuario} (id_usuario={id_usuario})")
            return redirect('/oficial')
        

        except Exception as e:
            print("Error al insertar en Supabase:", e)
            return redirect('/fail')
    
    return redirect('/')
    
#este manda correo pero aun no cambia contraseña
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


#PREGUNTAS PAL GAD 7 & PAL PHQ 9
def gad7(request):
    preguntas = [
        "Nerviosismo, ansiedad o tensión.",
        "Incapacidad para parar de preocuparte.",
        "Preocupación excesiva por diferentes cosas.",
        "Dificultad para relajarte.",
        "Inquietud que dificulta quedarse quieto.",
        "Irritabilidad o molestia fácil.",
        "Miedo a que algo terrible ocurra."
    ]
    
    
    return render(request, 'gad_7.html', {"preguntas": preguntas})



def gad7_enviar(request):
    if request.method == "POST":
        email_usuario = request.session.get("email") or request.session.get("nombre")
        if not email_usuario:
            return redirect('/fail')

        # Buscar id_usuario en Supabase
        usuario_query = supabase.table("usuarios").select("id_usuario").eq("email", email_usuario).execute()
        if not usuario_query.data:
            return redirect('/fail')
        id_usuario = usuario_query.data[0]["id_usuario"]

        # Diccionario para convertir número a texto
        valores_gad7 = {
            "0": "Nunca",
            "1": "Varios días",
            "2": "Más de la mitad de los días",
            "3": "Casi todos los días"
        }

        # Preparar datos para insertar
        data = {
            "id_usuario": id_usuario,
            "nerviosismo": valores_gad7.get(request.POST.get("q1")),
            "incapacidad": valores_gad7.get(request.POST.get("q2")),
            "preocupacion": valores_gad7.get(request.POST.get("q3")),
            "difi_relajacion": valores_gad7.get(request.POST.get("q4")),
            "inquietud": valores_gad7.get(request.POST.get("q5")),
            "irritabilidad": valores_gad7.get(request.POST.get("q6")),
            "miedo": valores_gad7.get(request.POST.get("q7")),
            "puntuacion": sum(int(request.POST.get(f"q{i}", 0)) for i in range(1, 8))  # suma de todas las respuestas
        }

        supabase.table("gad_7").insert(data).execute()
        return redirect('/oficial')





def phq9(request):
    preguntas = [
        "Poco interés o placer en hacer cosas.",
        "Sentirse decaído, deprimido o sin esperanza.",
        "Dificultad para dormir o dormir en exceso.",
        "Sentirse cansado o con poca energía.",
        "Poco apetito o comer en exceso.",
        "Sentirse mal consigo mismo o que ha fallado.",
        "Dificultad para concentrarse en cosas.",
        "Moverse o hablar tan lento que otros lo noten, o estar inquieto.",
        "Pensamientos de que estaría mejor muerto o de hacerse daño."
    ]
    return render(request, 'phq9.html', {"preguntas": preguntas})

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