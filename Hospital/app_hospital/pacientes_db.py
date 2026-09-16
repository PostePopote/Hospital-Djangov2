from django.db import connection


def obtener_pacientes():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM pacientes")

        columnas = [columna[0] for columna in cursor.description]

        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]


def obtener_paciente(id_paciente):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM pacientes WHERE id_paciente = %s",
            [id_paciente]
        )

        columnas = [columna[0] for columna in cursor.description]
        fila = cursor.fetchone()

        if fila is None:
            return None

        return dict(zip(columnas, fila))


def agregar_paciente_db(
    nombre,
    apellido,
    dni,
    fecha_nacimiento,
    sexo,
    direccion,
    telefono,
    email,
    grupo_sanguineo,
    contacto_emergencia,
    telefono_emergencia,
    obra_social,
    numero_afiliado,
    fecha_alta,
    estado
):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO pacientes
            (
                nombre,
                apellido,
                dni,
                fecha_nacimiento,
                sexo,
                direccion,
                telefono,
                email,
                grupo_sanguineo,
                contacto_emergencia,
                telefono_emergencia,
                obra_social,
                numero_afiliado,
                fecha_alta,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            [
                nombre,
                apellido,
                dni,
                fecha_nacimiento,
                sexo,
                direccion,
                telefono,
                email,
                grupo_sanguineo,
                contacto_emergencia,
                telefono_emergencia,
                obra_social,
                numero_afiliado,
                fecha_alta,
                estado
            ]
        )


def actualizar_paciente_db(
    id_paciente,
    nombre,
    apellido,
    dni,
    fecha_nacimiento,
    sexo,
    direccion,
    telefono,
    email,
    grupo_sanguineo,
    contacto_emergencia,
    telefono_emergencia,
    obra_social,
    numero_afiliado,
    fecha_alta,
    estado
):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE pacientes SET
                nombre = %s,
                apellido = %s,
                dni = %s,
                fecha_nacimiento = %s,
                sexo = %s,
                direccion = %s,
                telefono = %s,
                email = %s,
                grupo_sanguineo = %s,
                contacto_emergencia = %s,
                telefono_emergencia = %s,
                obra_social = %s,
                numero_afiliado = %s,
                fecha_alta = %s,
                estado = %s
            WHERE id_paciente = %s
            """,
            [
                nombre,
                apellido,
                dni,
                fecha_nacimiento,
                sexo,
                direccion,
                telefono,
                email,
                grupo_sanguineo,
                contacto_emergencia,
                telefono_emergencia,
                obra_social,
                numero_afiliado,
                fecha_alta,
                estado,
                id_paciente
            ]
        )