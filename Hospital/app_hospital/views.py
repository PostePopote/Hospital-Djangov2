from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .pacientes_db import (
    obtener_pacientes,
    agregar_paciente_db,
    obtener_paciente,
    actualizar_paciente_db
)

from .medicos_db import (
    obtener_medicos,
    obtener_medico,
    obtener_especialidades,
    agregar_medico_db,
    actualizar_medico_db
)

from .tratamientos_db import (
    obtener_tratamientos,
    obtener_tratamiento,
    agregar_tratamiento_db,
    actualizar_tratamiento_db
)

from .usuarios_db import obtener_usuario


# Login y logout
# Estas vistas verifican las credenciales y administran la sesión del usuario.

def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = obtener_usuario(username, password)

        if usuario:
            request.session['usuario_id'] = usuario['id_usuario']
            request.session['usuario_nombre'] = usuario['nombre']
            return redirect('home')
        else:
            error = 'Usuario o contraseña incorrectos'

    return render(request, 'app_hospital/login.html', {'error': error})


def logout_view(request):
    # Cierra la sesión eliminando sus datos y vuelve a la pantalla de acceso.
    request.session.flush()
    return redirect('login')


# Paginas basicas
# Vistas sencillas para mostrar la página principal y una respuesta de prueba.

def home(request):
    return render(request, 'app_hospital/home.html')


def saludo(request):
    return HttpResponse('Hola Mundo')


# Pacientes
# Estas vistas consultan, crean y actualizan pacientes mediante pacientes_db.

def pacientes(request):
    # Obtiene todos los pacientes para mostrarlos en el listado.
    lista_pacientes = obtener_pacientes()

    return render(
        request,
        'app_hospital/pacientes.html',
        {'pacientes': lista_pacientes}
    )


def agregar_paciente(request):

    if request.method == 'POST':

        agregar_paciente_db(
    # En POST, guarda los datos enviados por el formulario.
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            dni=request.POST.get('dni'),
            fecha_nacimiento=request.POST.get('fecha_nacimiento') or None,
            sexo=request.POST.get('sexo'),
            direccion=request.POST.get('direccion'),
            telefono=request.POST.get('telefono'),
            email=request.POST.get('email'),
            grupo_sanguineo=request.POST.get('grupo_sanguineo'),
            contacto_emergencia=request.POST.get('contacto_emergencia'),
            telefono_emergencia=request.POST.get('telefono_emergencia'),
            obra_social=request.POST.get('obra_social'),
            numero_afiliado=request.POST.get('numero_afiliado'),
            fecha_alta=request.POST.get('fecha_alta') or None,
            estado=request.POST.get('estado')
        )

        return redirect('pacientes')

    return render(
        request,
        'app_hospital/agregar_paciente.html'
    )


def editar_paciente(request, id_paciente):

    # Busca el paciente para cargarlo en el formulario de edición.
    paciente = obtener_paciente(id_paciente)

    if request.method == 'POST':

        actualizar_paciente_db(
            id_paciente=id_paciente,
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            dni=request.POST.get('dni'),
            fecha_nacimiento=request.POST.get('fecha_nacimiento') or None,
            sexo=request.POST.get('sexo'),
            direccion=request.POST.get('direccion'),
            telefono=request.POST.get('telefono'),
            email=request.POST.get('email'),
            grupo_sanguineo=request.POST.get('grupo_sanguineo'),
            contacto_emergencia=request.POST.get('contacto_emergencia'),
            telefono_emergencia=request.POST.get('telefono_emergencia'),
            obra_social=request.POST.get('obra_social'),
            numero_afiliado=request.POST.get('numero_afiliado'),
            fecha_alta=request.POST.get('fecha_alta') or None,
            estado=request.POST.get('estado')
        )

        return redirect('pacientes')

    return render(
        request,
        'app_hospital/editar_paciente.html',
        {'paciente': paciente}
    )


# Medicos
# Estas vistas muestran, crean y actualizan médicos y sus especialidades.

def medicos(request):

    # Carga los médicos disponibles para la página de listado.
    lista_medicos = obtener_medicos()

    return render(
        request,
        'app_hospital/medicos.html',
        {'medicos': lista_medicos}
    )


def agregar_medico(request):

    if request.method == 'POST':

    # Guarda el nuevo médico y regresa al listado.
        agregar_medico_db(
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            matricula=request.POST.get('matricula'),
            telefono=request.POST.get('telefono'),
            id_especialidad=request.POST.get('id_especialidad'),
            estado=request.POST.get('estado')
        )

        return redirect('medicos')

    lista_especialidades = obtener_especialidades()
    # En GET, carga las especialidades que ofrece el formulario.

    return render(
        request,
        'app_hospital/agregar_medico.html',
        {'especialidades': lista_especialidades}
    )


def editar_medico(request, id_medico):

    # Carga el médico y las especialidades disponibles para editarlo.
    medico = obtener_medico(id_medico)
    especialidades = obtener_especialidades()

    if request.method == 'POST':

        actualizar_medico_db(
            id_medico=id_medico,
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            matricula=request.POST.get('matricula'),
            telefono=request.POST.get('telefono'),
            id_especialidad=request.POST.get('id_especialidad'),
            estado=request.POST.get('estado')
        )

        return redirect('medicos')

    return render(
        request,
        'app_hospital/editar_medico.html',
        {
            'medico': medico,
            'especialidades': especialidades
        }
    )


# Tratamientos
# Estas vistas muestran y gestionan tratamientos asociados a pacientes y médicos.

def tratamientos(request):

    # Obtiene los tratamientos para presentar el listado.
    lista_tratamientos = obtener_tratamientos()

    return render(
        request,
        'app_hospital/tratamientos.html',
        {'tratamientos': lista_tratamientos}
    )


def agregar_tratamiento(request):

    if request.method == 'POST':

    # Registra el tratamiento con los datos enviados por el formulario.
            # En GET, prepara las opciones para asociar un paciente y un médico.
        agregar_tratamiento_db(
            id_paciente=request.POST.get('id_paciente'),
            id_medico=request.POST.get('id_medico'),
            descripcion=request.POST.get('descripcion'),
            fecha_inicio=request.POST.get('fecha_inicio') or None,
            fecha_fin=request.POST.get('fecha_fin') or None,
            observaciones=request.POST.get('observaciones'),
            estado=request.POST.get('estado')
        )

        return redirect('tratamientos')

    lista_pacientes = obtener_pacientes()
    lista_medicos = obtener_medicos()

    return render(
        request,
        'app_hospital/agregar_tratamiento.html',
        {
            'pacientes': lista_pacientes,
            'medicos': lista_medicos
        }
    )


def editar_tratamiento(request, id_tratamiento):

    # Carga el tratamiento y las opciones de asociación para su edición.
    tratamiento = obtener_tratamiento(id_tratamiento)
    lista_pacientes = obtener_pacientes()
    lista_medicos = obtener_medicos()

    if request.method == 'POST':

        actualizar_tratamiento_db(
            id_tratamiento=id_tratamiento,
            id_paciente=request.POST.get('id_paciente'),
            id_medico=request.POST.get('id_medico'),
            descripcion=request.POST.get('descripcion'),
            fecha_inicio=request.POST.get('fecha_inicio') or None,
            fecha_fin=request.POST.get('fecha_fin') or None,
            observaciones=request.POST.get('observaciones'),
            estado=request.POST.get('estado')
        )

        return redirect('tratamientos')

    return render(
        request,
        'app_hospital/editar_tratamiento.html',
        {
            'tratamiento': tratamiento,
            'pacientes': lista_pacientes,
            'medicos': lista_medicos
        }
    )