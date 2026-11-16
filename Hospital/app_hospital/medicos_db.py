from django.db import connection

# Obtiene todos los médicos junto con el nombre de su especialidad
def obtener_medicos():

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT
                m.id_medico,
                m.nombre,
                m.apellido,
                m.matricula,
                m.telefono,
                e.nombre AS especialidad
                FROM medicos m
                JOIN especialidades e
                ON m.id_especialidad = e.id_especialidad
        """)

        # Obtiene los nombres de las columnas para crear diccionarios
        columnas = [columna[0] for columna in cursor.description]

        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]


# Obtiene un médico específico mediante su ID
def obtener_medico(id_medico):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT *
            FROM medicos
            WHERE id_medico = %s
            """,
            [id_medico]
        )

        columnas = [columna[0] for columna in cursor.description]

        fila = cursor.fetchone()

        # Si no existe el médico, devuelve None
        if fila is None:
            return None

        return dict(zip(columnas, fila))


# Obtiene todas las especialidades disponibles
def obtener_especialidades():

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT *
            FROM especialidades
        """)

        # Obtiene los nombres de las columnas para crear diccionarios
        columnas = [columna[0] for columna in cursor.description]

        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]


# Agrega un nuevo médico a la base de datos
def agregar_medico_db(
    nombre,
    apellido,
    matricula,
    telefono,
    id_especialidad,
    estado
):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            INSERT INTO medicos
            (
                nombre,
                apellido,
                matricula,
                telefono,
                id_especialidad,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            [
                nombre,
                apellido,
                matricula,
                telefono,
                id_especialidad,
                estado
            ]
        )


# Actualiza los datos de un médico existente
def actualizar_medico_db(
    id_medico,
    nombre,
    apellido,
    matricula,
    telefono,
    id_especialidad,
    estado
):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            UPDATE medicos
            SET
                nombre = %s,
                apellido = %s,
                matricula = %s,
                telefono = %s,
                id_especialidad = %s,
                estado = %s
            WHERE id_medico = %s
            """,
            [
                nombre,
                apellido,
                matricula,
                telefono,
                id_especialidad,
                estado,
                id_medico
            ]
        )