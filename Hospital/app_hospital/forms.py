from django import forms
from django.db import connection


def traer_opciones(consulta):
    # Ejecuta una consulta y devuelve una lista de (id, texto) para los select
    with connection.cursor() as cursor:
        cursor.execute(consulta)
        return [(fila[0], fila[1]) for fila in cursor.fetchall()]


class FormularioBase(forms.Form):
    # Agrega las clases de Bootstrap a todos los campos
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nombre_campo, campo in self.fields.items():
            if isinstance(campo.widget, forms.Select):
                campo.widget.attrs['class'] = 'form-select'
            else:
                campo.widget.attrs['class'] = 'form-control'


class PacienteForm(FormularioBase):
    nombre = forms.CharField(label='Nombre', max_length=100)
    apellido = forms.CharField(label='Apellido', max_length=100)
    dni = forms.CharField(label='DNI', max_length=20)
    fecha_nacimiento = forms.DateField(
        label='Fecha de Nacimiento',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
    )
    sexo = forms.CharField(label='Sexo', max_length=20, required=False)
    direccion = forms.CharField(label='Direccion', max_length=255, required=False)
    telefono = forms.CharField(label='Telefono', max_length=30, required=False)
    email = forms.EmailField(label='Email', max_length=100, required=False)
    grupo_sanguineo = forms.CharField(label='Grupo Sanguineo', max_length=5, required=False)
    contacto_emergencia = forms.CharField(label='Contacto de Emergencia', max_length=100, required=False)
    telefono_emergencia = forms.CharField(label='Telefono de Emergencia', max_length=30, required=False)
    obra_social = forms.CharField(label='Obra Social', max_length=100, required=False)
    numero_afiliado = forms.CharField(label='Numero de Afiliado', max_length=50, required=False)
    fecha_alta = forms.DateField(
        label='Fecha de Alta',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
    )
    estado = forms.CharField(label='Estado', max_length=20, required=False)


class MedicoForm(FormularioBase):
    nombre = forms.CharField(label='Nombre', max_length=100)
    apellido = forms.CharField(label='Apellido', max_length=100)
    matricula = forms.CharField(label='Matricula', max_length=50)
    telefono = forms.CharField(label='Telefono', max_length=30, required=False)
    id_especialidad = forms.ChoiceField(label='Especialidad')
    estado = forms.CharField(label='Estado', max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Carga las especialidades desde la base de datos
        self.fields['id_especialidad'].choices = traer_opciones(
            "SELECT id_especialidad, nombre FROM especialidades"
        )


class TratamientoForm(FormularioBase):
    id_paciente = forms.ChoiceField(label='Paciente')
    id_medico = forms.ChoiceField(label='Medico')
    descripcion = forms.CharField(label='Descripcion', max_length=255)
    fecha_inicio = forms.DateField(
        label='Fecha Inicio',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
    )
    fecha_fin = forms.DateField(
        label='Fecha Fin',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
    )
    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )
    estado = forms.CharField(label='Estado', max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Carga pacientes y medicos desde la base de datos
        self.fields['id_paciente'].choices = traer_opciones(
            "SELECT id_paciente, CONCAT(nombre, ' ', apellido) FROM pacientes"
        )
        self.fields['id_medico'].choices = traer_opciones(
            "SELECT id_medico, CONCAT(nombre, ' ', apellido) FROM medicos"
        )