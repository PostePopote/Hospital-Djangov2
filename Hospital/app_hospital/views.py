from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from . import forms, usuarios_db
from .decorador import solo_admin

# Convierte el resultado del cursor en una lista de diccionarios
def dictfetchall(cursor):
    columnas = [col[0] for col in cursor.description]
    return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

# Login
def login(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = usuarios_db.buscar_usuario(username, password)
        if user:
            # guardo los datos en la sesion
            request.session['username'] = user['username']
            request.session['nivel'] = user['nivel']
            return redirect('home')
        else:
            error = 'Usuario o contrasena incorrectos'
    return render(request, 'app_hospital/login.html', {'error': error})

def registro(request):
    error = ''
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            error = 'Las contrasenas no coinciden'
        elif usuarios_db.existe_usuario(username):
            error = 'Ese usuario ya existe'
        else:
            usuarios_db.crear_usuario(nombre, username, password)
            return redirect('login')
    return render(request, 'app_hospital/registro.html', {'error': error})

def logout(request):
    # borro todo lo que habia en la sesion (usuario y nivel)
    request.session.flush()
    return redirect('/')

# Paginas normales

# Muestra la pagina principal
def home(request):
    return render(request, 'app_hospital/home.html')

# Pagina utilizada para comprobar que Django funciona
def saludo(request):
    return HttpResponse('Hola Mundo')

# Pacientes

# Trae los pacientes de la base de datos y los muestra
@solo_admin
def pacientes(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM pacientes")
        lista_pacientes = dictfetchall(cursor)
    return render(
        request,
        'app_hospital/pacientes.html',
        {'pacientes': lista_pacientes}
    )

# Muestra y procesa el formulario para agregar un paciente
@solo_admin
def agregar_paciente(request):
    if request.method == 'POST':
        form = forms.PacienteForm(request.POST)
        # Si los datos son validos, se guardan en la base de datos
        if form.is_valid():
            datos = form.cleaned_data
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
                        datos['nombre'],
                        datos['apellido'],
                        datos['dni'],
                        datos['fecha_nacimiento'],
                        datos['sexo'],
                        datos['direccion'],
                        datos['telefono'],
                        datos['email'],
                        datos['grupo_sanguineo'],
                        datos['contacto_emergencia'],
                        datos['telefono_emergencia'],
                        datos['obra_social'],
                        datos['numero_afiliado'],
                        datos['fecha_alta'],
                        datos['estado'],
                    ]
                )
            return redirect('pacientes')
    else:
        form = forms.PacienteForm()
    return render(
        request,
        'app_hospital/agregar_paciente.html',
        {'form': form}
    )


# Muestra y actualiza los datos de un paciente
@solo_admin
def editar_paciente(request, id_paciente):
    if request.method == 'POST':
        form = forms.PacienteForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE pacientes SET
                        nombre = %s, apellido = %s, dni = %s, fecha_nacimiento = %s,
                        sexo = %s, direccion = %s, telefono = %s, email = %s,
                        grupo_sanguineo = %s, contacto_emergencia = %s, telefono_emergencia = %s,
                        obra_social = %s, numero_afiliado = %s, fecha_alta = %s, estado = %s
                    WHERE id_paciente = %s
                    """,
                    [
                        datos['nombre'],
                        datos['apellido'],
                        datos['dni'],
                        datos['fecha_nacimiento'],
                        datos['sexo'],
                        datos['direccion'],
                        datos['telefono'],
                        datos['email'],
                        datos['grupo_sanguineo'],
                        datos['contacto_emergencia'],
                        datos['telefono_emergencia'],
                        datos['obra_social'],
                        datos['numero_afiliado'],
                        datos['fecha_alta'],
                        datos['estado'],
                        id_paciente,
                    ]
                )
            return redirect('pacientes')
    else:
        # Trae el paciente y lo carga en el formulario
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pacientes WHERE id_paciente = %s", [id_paciente])
            paciente = dictfetchall(cursor)[0]
        form = forms.PacienteForm(initial=paciente)
    return render(
        request,
        'app_hospital/editar_paciente.html',
        {'form': form}
    )

# Medicos

# Trae los medicos de la base de datos y los muestra
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
    return render(
        request,
        'app_hospital/medicos.html',
        {'medicos': lista_medicos}
    )

# Muestra y procesa el formulario para agregar un medico
@solo_admin
def agregar_medico(request):
    if request.method == 'POST':
        form = forms.MedicoForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO medicos
                    (nombre, apellido, matricula, telefono, id_especialidad, estado)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    [
                        datos['nombre'],
                        datos['apellido'],
                        datos['matricula'],
                        datos['telefono'],
                        datos['id_especialidad'],
                        datos['estado'],
                    ]
                )
            return redirect('medicos')
    else:
        form = forms.MedicoForm()
    return render(
        request,
        'app_hospital/agregar_medico.html',
        {'form': form}
    )

# Muestra y actualiza los datos de un medico
@solo_admin
def editar_medico(request, id_medico):
    if request.method == 'POST':
        form = forms.MedicoForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE medicos SET
                        nombre = %s, apellido = %s, matricula = %s, telefono = %s,
                        id_especialidad = %s, estado = %s
                    WHERE id_medico = %s
                    """,
                    [
                        datos['nombre'],
                        datos['apellido'],
                        datos['matricula'],
                        datos['telefono'],
                        datos['id_especialidad'],
                        datos['estado'],
                        id_medico,
                    ]
                )
            return redirect('medicos')
    else:
        # Trae el medico y lo carga en el formulario
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM medicos WHERE id_medico = %s", [id_medico])
            medico = dictfetchall(cursor)[0]
        form = forms.MedicoForm(initial=medico)
    return render(
        request,
        'app_hospital/editar_medico.html',
        {'form': form}
    )

# Tratamientos

# Trae los tratamientos de la base de datos y los muestra
@solo_admin
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
    return render(
        request,
        'app_hospital/tratamientos.html',
        {'tratamientos': lista_tratamientos}
    )

# Muestra y procesa el formulario para agregar un tratamiento
@solo_admin
def agregar_tratamiento(request):
    if request.method == 'POST':
        form = forms.TratamientoForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tratamientos
                    (id_paciente, id_medico, descripcion, fecha_inicio, fecha_fin, observaciones, estado)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    [
                        datos['id_paciente'],
                        datos['id_medico'],
                        datos['descripcion'],
                        datos['fecha_inicio'],
                        datos['fecha_fin'],
                        datos['observaciones'],
                        datos['estado'],
                    ]
                )
            return redirect('tratamientos')
    else:
        form = forms.TratamientoForm()
    return render(
        request,
        'app_hospital/agregar_tratamiento.html',
        {'form': form}
    )

# Muestra y actualiza los datos de un tratamiento
@solo_admin
def editar_tratamiento(request, id_tratamiento):
    if request.method == 'POST':
        form = forms.TratamientoForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tratamientos SET
                        id_paciente = %s, id_medico = %s, descripcion = %s,
                        fecha_inicio = %s, fecha_fin = %s, observaciones = %s, estado = %s
                    WHERE id_tratamiento = %s
                    """,
                    [
                        datos['id_paciente'],
                        datos['id_medico'],
                        datos['descripcion'],
                        datos['fecha_inicio'],
                        datos['fecha_fin'],
                        datos['observaciones'],
                        datos['estado'],
                        id_tratamiento,
                    ]
                )
            return redirect('tratamientos')
    else:
        # Trae el tratamiento y lo carga en el formulario
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tratamientos WHERE id_tratamiento = %s", [id_tratamiento])
            tratamiento = dictfetchall(cursor)[0]
        form = forms.TratamientoForm(initial=tratamiento)
    return render(
        request,
        'app_hospital/editar_tratamiento.html',
        {'form': form}
    )