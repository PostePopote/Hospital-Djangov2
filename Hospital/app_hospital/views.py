from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from functools import wraps


def dictfetchall(cursor):
    # Convierte el resultado del cursor en una lista de diccionarios
    # asi los templates pueden seguir usando {{ objeto.campo }}
    columnas = [col[0] for col in cursor.description]
    return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]


# ---------- DECORADOR PARA PROTEGER VISTAS ----------

def login_requerido(vista):
    @wraps(vista)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('login')
        return vista(request, *args, **kwargs)
    return wrapper


# ---------- LOGIN / LOGOUT ----------

def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM usuarios WHERE username = %s AND password = %s",
                [username, password]
            )
            usuario = dictfetchall(cursor)

        if usuario:
            # Guardamos los datos del usuario en la sesion
            request.session['usuario_id'] = usuario[0]['id_usuario']
            request.session['usuario_nombre'] = usuario[0]['nombre']
            return redirect('index')
        else:
            error = 'Usuario o contraseña incorrectos'

    return render(request, 'app_hospital/login.html', {'error': error})


def logout_view(request):
    request.session.flush()
    return redirect('login')


# ---------- PAGINAS BASICAS ----------

def home(request):
    return render(request, 'app_hospital/home.html')


def saludo(request):
    return HttpResponse('Hola Mundo')


def index(request):
    return render(request, 'app_hospital/index.html')


# ---------- PACIENTES ----------

@login_requerido
def pacientes(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM pacientes")
        lista_pacientes = dictfetchall(cursor)

    return render(request, 'app_hospital/pacientes.html', {'pacientes': lista_pacientes})


@login_requerido
def agregar_paciente(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO pacientes
                (nombre, apellido, dni, fecha_nacimiento, sexo, direccion, telefono,
                 email, grupo_sanguineo, contacto_emergencia, telefono_emergencia,
                 obra_social, numero_afiliado, fecha_alta, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [
                    request.POST.get('nombre'),
                    request.POST.get('apellido'),
                    request.POST.get('dni'),
                    request.POST.get('fecha_nacimiento') or None,
                    request.POST.get('sexo'),
                    request.POST.get('direccion'),
                    request.POST.get('telefono'),
                    request.POST.get('email'),
                    request.POST.get('grupo_sanguineo'),
                    request.POST.get('contacto_emergencia'),
                    request.POST.get('telefono_emergencia'),
                    request.POST.get('obra_social'),
                    request.POST.get('numero_afiliado'),
                    request.POST.get('fecha_alta') or None,
                    request.POST.get('estado'),
                ]
            )
        return redirect('pacientes')

    return render(request, 'app_hospital/agregar_paciente.html')


# ---------- MEDICOS ----------

@login_requerido
def medicos(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT m.id_medico, m.nombre, m.apellido, m.matricula, m.telefono,
                   e.nombre AS especialidad
            FROM medicos m
            JOIN especialidades e ON m.id_especialidad = e.id_especialidad
            """
        )
        lista_medicos = dictfetchall(cursor)

    return render(request, 'app_hospital/medicos.html', {'medicos': lista_medicos})


@login_requerido
def agregar_medico(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM especialidades")
        lista_especialidades = dictfetchall(cursor)

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO medicos
                (nombre, apellido, matricula, telefono, id_especialidad, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                [
                    request.POST.get('nombre'),
                    request.POST.get('apellido'),
                    request.POST.get('matricula'),
                    request.POST.get('telefono'),
                    request.POST.get('id_especialidad'),
                    request.POST.get('estado'),
                ]
            )
        return redirect('medicos')

    return render(request, 'app_hospital/agregar_medico.html', {'especialidades': lista_especialidades})


# ---------- TRATAMIENTOS ----------

@login_requerido
def tratamientos(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT t.id_tratamiento,
                   CONCAT(p.nombre, ' ', p.apellido) AS paciente,
                   t.descripcion,
                   CONCAT(md.nombre, ' ', md.apellido) AS medico,
                   t.fecha_inicio, t.fecha_fin, t.observaciones, t.estado
            FROM tratamientos t
            JOIN pacientes p ON t.id_paciente = p.id_paciente
            JOIN medicos md ON t.id_medico = md.id_medico
            """
        )
        lista_tratamientos = dictfetchall(cursor)

    return render(request, 'app_hospital/tratamientos.html', {'tratamientos': lista_tratamientos})


@login_requerido
def agregar_tratamiento(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_paciente, nombre, apellido FROM pacientes")
        lista_pacientes = dictfetchall(cursor)

        cursor.execute("SELECT id_medico, nombre, apellido FROM medicos")
        lista_medicos = dictfetchall(cursor)

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tratamientos
                (id_paciente, id_medico, descripcion, fecha_inicio, fecha_fin, observaciones, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                [
                    request.POST.get('id_paciente'),
                    request.POST.get('id_medico'),
                    request.POST.get('descripcion'),
                    request.POST.get('fecha_inicio') or None,
                    request.POST.get('fecha_fin') or None,
                    request.POST.get('observaciones'),
                    request.POST.get('estado'),
                ]
            )
        return redirect('tratamientos')

    return render(request, 'app_hospital/agregar_tratamiento.html', {
        'pacientes': lista_pacientes,
        'medicos': lista_medicos,
    })