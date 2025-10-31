# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from supabase import create_client, Client
from datetime import datetime
from dateutil import parser

# ==========================================================
# 🔗 CONEXIÓN A SUPABASE
# ==========================================================
url = "https://cixtrfcwsweaxtliwdgc.supabase.co"
# ⚠️ Recomendado: mover esta clave a un archivo .env
key = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpeHRyZmN3c3dlYXh0bGl3ZGdjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAxMTA2MjUsImV4cCI6MjA3NTY4NjYyNX0."
    "5hGTCUa9t7jghSE5hW-o-2vBPDTmyYZu7OzZwHgj0uA"
)

supabase: Client = create_client(url, key)

# ==========================================================
# 🌐 VISTAS DE PÁGINAS ESTÁTICAS
# ==========================================================
def paginator(request):
    return render(request, 'ingreso.html')

def paginator2(request):
    try:
        # Obtener las carreras de la base de datos
        response = supabase.table("carrera").select("id_carrera, nombre_carrera").execute()
        carreras = response.data if response.data else []
        
        # Renderizar la página y pasar las carreras al contexto
        return render(request, 'CrearUsuario.html', {"carreras": carreras})
    except Exception as e:
        print("Error al obtener carreras:", e)
        return render(request, 'CrearUsuario.html', {"carreras": []})

def paginatorfail(request):
    return render(request, 'fail.html')

def introduccion(request):
    return render(request, 'introduccion.html')

# ==========================================================
# 👤 REGISTRO DE USUARIO
# ==========================================================
def usercreate(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        rut = request.POST.get('rut')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        telefono = request.POST.get('telefono')
        password = request.POST.get('password')
        id_carrera = request.POST.get('id_carrera')  # Obtener la carrera seleccionada

        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {"data": {"nombre": nombre, "apellido": apellido}} 
            })

            if response.user:
                data = {
                    "nombre": nombre,
                    "apellido": apellido,
                    "email": email,
                    "fecha_nacimiento": fecha_nacimiento,
                    "telefono": telefono,
                    "rut": rut,
                    "id_carrera": id_carrera  # Incluir la carrera seleccionada
                }
                # Insertar los datos del usuario incluyendo la carrera
                supabase.table("usuarios").insert(data).execute()
            else:
                return redirect('/crear')
        except Exception as e:
            print(e)
            return redirect('/crear')
    return redirect('/')


# ==========================================================
# 🔐 DECORADOR: PROTECCIÓN POR TOKEN DE SUPABASE
# ==========================================================
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

# ==========================================================
# 🔑 INICIO DE SESIÓN
# ==========================================================
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

# ==========================================================
# 🏠 PÁGINAS PROTEGIDAS
# ==========================================================
@supabase_login_required
def oficial(request):
    nombre = request.session.get("nombre", "Usuario")
    return render(request, "oficial.html", {"nombre": nombre})

@supabase_login_required
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

@supabase_login_required
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

def interpretar_phq9(puntuacion):
    if puntuacion <= 4:
        return "Sin depresión"
    elif 5 <= puntuacion <= 9:
        return "Depresión leve"
    elif 10 <= puntuacion <= 14:
        return "Depresión moderada"
    elif 15 <= puntuacion <= 19:
        return "Depresión moderadamente severa"
    else:  # 20 - 27
        return "Depresión severa"

def interpretar_gad7(puntuacion):
    if puntuacion <= 4:
        return "Sin ansiedad"
    elif 5 <= puntuacion <= 9:
        return "Ansiedad leve"
    elif 10 <= puntuacion <= 14:
        return "Ansiedad moderada"
    else:  # 15 - 21
        return "Ansiedad severa"
    

@supabase_login_required
def ver_test(request):
    email_usuario = request.session.get("email")
    if not email_usuario:
        return redirect('/fail')

    try:
        usuario_query = supabase.table("usuarios").select("id_usuario").eq("email", email_usuario).execute()
        if not usuario_query.data:
            return redirect('/fail')

        id_usuario = usuario_query.data[0]["id_usuario"]

        phq9_query = (
            supabase.table("phq_9")
            .select("puntuacion, fecha_creacion")
            .eq("id_usuario", id_usuario)
            .order("fecha_creacion", desc=True)
            .execute()
        )
        phq9_tests = phq9_query.data if phq9_query.data else []
        # Añadir interpretación a cada resultado
        for test in phq9_tests:
            if isinstance(test['fecha_creacion'], str):
                test['fecha_creacion'] = parser.isoparse(test['fecha_creacion'])
            test['interpretacion'] = interpretar_phq9(test['puntuacion'])

        gad7_query = (
            supabase.table("gad_7")
            .select("puntuacion, fecha_creacion")
            .eq("id_usuario", id_usuario)
            .order("fecha_creacion", desc=True)
            .execute()
        )
        gad7_tests = gad7_query.data if gad7_query.data else []
        for test in gad7_tests:
            if isinstance(test['fecha_creacion'], str):
                test['fecha_creacion'] = parser.isoparse(test['fecha_creacion'])
            test['interpretacion'] = interpretar_gad7(test['puntuacion'])
            
        context = {
            "nombre": request.session.get("nombre"),
            "phq9_tests": phq9_tests,
            "gad7_tests": gad7_tests,
        }

        return render(request, "ver_test.html", context)

    except Exception as e:
        print("Error al cargar resultados:", e)
        return redirect('/fail')
    
@supabase_login_required
def ver_perfil(request):
    email_usuario = request.session.get("email")
    if not email_usuario:
        return redirect('/fail')

    try:
        # Obtener los datos del usuario desde la tabla 'usuarios'
        usuario_query = supabase.table("usuarios").select("*").eq("email", email_usuario).execute()
        if not usuario_query.data:
            return redirect('/fail')

        usuario_data = usuario_query.data[0]
        
        # Obtener el id_carrera del usuario
        id_carrera = usuario_data.get("id_carrera")
        carrera_nombre = "NO INFORMADA AÚN"  # Valor por defecto en caso de que no tenga carrera asignada

        if id_carrera:
            # Obtener el nombre de la carrera desde la tabla 'carrera'
            carrera_query = supabase.table("carrera").select("nombre_carrera").eq("id_carrera", id_carrera).execute()
            if carrera_query.data:
                carrera_nombre = carrera_query.data[0].get("nombre_carrera")

        # Convertir la fecha de nacimiento de varchar a datetime
        fecha_nacimiento_str = usuario_data["fecha_nacimiento"]
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d")  # Formato adecuado para '2000-11-01'

        # Calcular la edad
        today = datetime.today()
        edad = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        # Agregar al contexto la fecha de nacimiento, la edad y la carrera
        context = {
            "nombre": usuario_data["nombre"],
            "apellido": usuario_data["apellido"],
            "email": usuario_data["email"],
            "fecha_nacimiento": fecha_nacimiento_str,
            "edad": edad,  # Edad calculada
            "telefono": usuario_data["telefono"],
            "rut": usuario_data["rut"],
            "carrera": carrera_nombre,  # Carrera del usuario
        }

        return render(request, "ver_perfil.html", context)

    except Exception as e:
        print("Error al cargar el perfil:", e)
        return redirect('/fail')
    



    
# ==========================================================
# 📋 TEST DE RECONOCIMIENTO
# ==========================================================

@supabase_login_required
def Test_reconocimiento(request):
    try:
        response = supabase.table("carrera").select("id_carrera, nombre_carrera").execute()
        carreras = response.data if response.data else []
    except Exception as e:
        print("Error al obtener carreras:", e)
        carreras = []

    return render(request, 'Test_reconocimiento.html', {"carreras": carreras})


@supabase_login_required
def TestRecco_enviar(request):
    if request.method == "POST":
        carrera = request.POST.get('carrera')
        motivo_estudio = request.POST.get('motivo_estudio')
        año_estudio = request.POST.get('año_estudio')
        intereses = request.POST.get('intereses')
        malestar = request.POST.get('malestar')
        expect_inicial = request.POST.get('expect_inicial')
        razon = request.POST.get('razon')

        email_usuario = request.session.get("email") or request.session.get("nombre")
        if not email_usuario:
            return redirect('/fail')

        try:
            # Obtener el ID del usuario desde la base de datos
            usuario_query = supabase.table("usuarios").select("id_usuario").eq("email", email_usuario).execute()
            if not usuario_query.data:
                return redirect('/fail')

            id_usuario = usuario_query.data[0]["id_usuario"]
 
            # Crear el diccionario de datos para la tabla Test_reconocimiento
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

            # Insertar los datos en la tabla Test_reconocimiento
            supabase.table("Test_reconocimiento").insert(data).execute()

            print(f"✅ Test guardado para {email_usuario} (id={id_usuario})")
            return redirect('/oficial')

        except Exception as e:
            print("Error al insertar en Supabase:", e)
            return redirect('/fail')

    return redirect('/')

# ==========================================================
# 🔄 TEST GAD-7
# ==========================================================
def gad7_enviar(request):
    if request.method == "POST":
        email_usuario = request.session.get("email") or request.session.get("nombre")
        if not email_usuario:
            return redirect('/fail')

        usuario_query = supabase.table("usuarios").select("id_usuario").eq("email", email_usuario).execute()
        if not usuario_query.data:
            return redirect('/fail')

        id_usuario = usuario_query.data[0]["id_usuario"]

        valores_gad7 = {
            "0": "Nunca",
            "1": "Varios días",
            "2": "Más de la mitad de los días",
            "3": "Casi todos los días"
        }

        data = {
            "id_usuario": id_usuario,
            "nerviosismo": valores_gad7.get(request.POST.get("q1")),
            "incapacidad": valores_gad7.get(request.POST.get("q2")),
            "preocupacion": valores_gad7.get(request.POST.get("q3")),
            "difi_relajacion": valores_gad7.get(request.POST.get("q4")),
            "inquietud": valores_gad7.get(request.POST.get("q5")),
            "irritabilidad": valores_gad7.get(request.POST.get("q6")),
            "miedo": valores_gad7.get(request.POST.get("q7")),
            "puntuacion": sum(int(request.POST.get(f"q{i}", 0)) for i in range(1, 8))
        }

        supabase.table("gad_7").insert(data).execute()
        return redirect('/oficial')

# ==========================================================
# 🔄 TEST PHQ-9
# ==========================================================

def phq9_enviar(request):
    if request.method == "POST":
        email_usuario = request.session.get("email") or request.session.get("nombre")
        if not email_usuario:
            return redirect('/fail')

        usuario_query = supabase.table("usuarios").select("id_usuario").eq("email", email_usuario).execute()
        if not usuario_query.data:
            return redirect('/fail')

        id_usuario = usuario_query.data[0]["id_usuario"]

        valores_phq9 = {
            "0": "Nunca",
            "1": "Varios días",
            "2": "Más de la mitad de los días",
            "3": "Casi todos los días"
        }

        data = {
            "id_usuario": id_usuario,
            "Bajo_interes": valores_phq9.get(request.POST.get("q1")),
            "deprimido": valores_phq9.get(request.POST.get("q2")),
            "diff_dormir": valores_phq9.get(request.POST.get("q3")),
            "descontrol_apetito": valores_phq9.get(request.POST.get("q4")),
            "baja_autoestima": valores_phq9.get(request.POST.get("q5")),
            "baja_concentracion": valores_phq9.get(request.POST.get("q6")),
            "inquietud": valores_phq9.get(request.POST.get("q7")),
            "pensamientos_autodañinos": valores_phq9.get(request.POST.get("q8")),
            "puntuacion": sum(int(request.POST.get(f"q{i}", 0)) for i in range(1, 9))
        }

        supabase.table("phq_9").insert(data).execute()
        return redirect('/oficial')
    
# ==========================================================
# 📧 Super test
# ==========================================================    

@supabase_login_required
def super_test(request):
   # nombre = request.session.get("nombre", "Usuario")
    return render(request, "super_test.html")

@supabase_login_required
def situacion_familiar_enviar(request):
    if request.method == "POST":
        # Obtener email del usuario logueado
        email_usuario = request.session.get("email") or request.session.get("nombre")
        if not email_usuario:
            return redirect('/fail')

        # Buscar id_usuario en Supabase
        usuario_query = supabase.table("usuarios").select("id_usuario").eq("email", email_usuario).execute()
        if not usuario_query.data:
            return redirect('/fail')
        id_usuario = usuario_query.data[0]["id_usuario"]

        # Preparar los datos del formulario
        data = {
            "id_usuario": id_usuario,
            "estado_civil": request.POST.get("Estado_civil"),
            "convivencia": request.POST.get("convivencia"),
            "apoyo_familiar": request.POST.get("Apoyo"),
            "problema_familiar": request.POST.get("problema_familiar"),
            "relacion_familiar": request.POST.get("relacion_familiar"),
        }

        # Insertar en la tabla situacion_familiar
        response = supabase.table("situacion_familiar").insert(data).execute()

        # Verificar errores de inserción
        if hasattr(response, "error") and response.error:
            return render(request, "super_test.html", {"error_message": "Error al guardar los datos."})

        return redirect('/super_test_1')

    # Si el método no es POST
    return redirect('/fail')


@supabase_login_required
def super_test_1(request):
   # nombre = request.session.get("nombre", "Usuario")
    return render(request, "super_test1.html")



@supabase_login_required
def super_test_2(request):
   # nombre = request.session.get("nombre", "Usuario")
    return render(request, "super_test2.html")

def salud_fisica_enviar(request):
    if request.method == "POST":
        # Obtener email o nombre del usuario desde la sesión
        email_usuario = request.session.get("email") or request.session.get("nombre")
        if not email_usuario:
            return redirect('/fail')

        # Buscar id_usuario en la tabla usuarios
        usuario_query = supabase.table("usuarios").select("id_usuario").eq("email", email_usuario).execute()
        if not usuario_query.data:
            return redirect('/fail')

        id_usuario = usuario_query.data[0]["id_usuario"]

        # Capturar datos del formulario
        salud_fisica = request.POST.get("salud_fisica")
        consumo_medicamentos = request.POST.get("consumo_medicamentos")
        alergias = request.POST.get("alergias")
        problemas_vision = request.POST.get("problemas_vision")
        problemas_audicion = request.POST.get("problemas_audicion")
        ejercicio = request.POST.get("ejercicio")
        hospitalizaciones_cirugias = request.POST.get("hospitalizaciones")

        # Validar datos obligatorios
        if not salud_fisica:
            return render(request, "oficial.html", {"error_message": "Debes ingresar tu estado de salud."})

        # Crear diccionario para insertar
        data = {
            "salud_fisica": salud_fisica,
            "consumo_medicamentos": consumo_medicamentos,
            "alergias": alergias,
            "problemas_vision": problemas_vision,
            "problemas_audicion": problemas_audicion,
            "ejercicio": ejercicio,
            "hospitalizaciones_cirugias": hospitalizaciones_cirugias,
            "id_usuario": id_usuario
        }

        try:
            supabase.table("salud_fisica").insert(data).execute()
            # Redirigir a super_test_2 usando el name de la URL
            return redirect("super_test_2")
        except Exception as e:
            print("Error al guardar en Supabase:", e)
            return render(request, "oficial.html", {"error_message": "Error al guardar los datos."})

    # Si no es POST, renderiza el formulario
    return render(request, "oficial.html")




# ==========================================================
# 📧 RECUPERAR CONTRASEÑA
# ==========================================================
def recuperar_contraseña(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            supabase.auth.reset_password_for_email(email)
            message = (
                "Se ha enviado un correo con las instrucciones para restablecer tu contraseña. "
                "(Revisa también la carpeta de SPAM)."
            )
        except Exception as e:
            print("Error al enviar correo:", e)
            message = (
                "El correo electrónico no está registrado o hubo un problema. "
                "Verifica el correo e inténtalo nuevamente."
            )

        return JsonResponse({'message': message})

    return render(request, 'recuperar_contraseña.html')

# ==========================================================
# 🚪 CERRAR SESIÓN
# ==========================================================
def logout_view(request):
    request.session.flush()
    return redirect('/')

# ==========================================================
# 💤 FUNCIONES DE CAMBIO DE CONTRASEÑA (NO EN USO ACTUALMENTE)
# ==========================================================
# --- 1. Mostrar la página de cambio de contraseña ---
# def mostrarCambioPassword(request):
#     token = request.GET.get("access_token")  # token enviado por Supabase en el link
#
#     if not token:
#         # Si no hay token, redirige al inicio
#         return redirect('/')
#
#     # Si hay token, muestra la página cambioPass.html
#     return render(request, 'CambioPass.html', {"token": token})
#
#
# --- 2. Procesar el cambio de contraseña ---
# def HacercambiarPassword(request):
#     if request.method == "POST":
#         token = request.POST.get("token")
#         nueva_contrasena = request.POST.get("password")
#
#         if not token or not nueva_contrasena:
#             return render(request, 'recuperar_contraseña.html', {
#                 "error": "Faltan datos para cambiar la contraseña."
#             })
#
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
#
#     # Si no es POST, vuelve al inicio
#     return redirect('/')
#
#
# --- Función de salida (no funcional actualmente) ---
# def salir(request):
#     try:
#         del request.session['uid']
#     except KeyError:
#         pass
#     return redirect('/')
