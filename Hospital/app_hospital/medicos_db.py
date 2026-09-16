from django.db import connection


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

        columnas = [columna[0] for columna in cursor.description]

        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]


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

        if fila is None:
            return None

        return dict(zip(columnas, fila))


def obtener_especialidades():

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT *
            FROM especialidades
        """)

        columnas = [columna[0] for columna in cursor.description]

        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]


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