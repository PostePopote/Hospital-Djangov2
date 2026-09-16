from django.db import connection


def obtener_tratamientos():

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT
                t.id_tratamiento,
                CONCAT(p.nombre, ' ', p.apellido) AS paciente,
                t.descripcion,
                CONCAT(md.nombre, ' ', md.apellido) AS medico,
                t.fecha_inicio,
                t.fecha_fin,
                t.observaciones,
                t.estado
            FROM tratamientos t
            JOIN pacientes p
                ON t.id_paciente = p.id_paciente
            JOIN medicos md
                ON t.id_medico = md.id_medico
        """)

        columnas = [columna[0] for columna in cursor.description]

        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]


def obtener_tratamiento(id_tratamiento):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT *
            FROM tratamientos
            WHERE id_tratamiento = %s
            """,
            [id_tratamiento]
        )

        columnas = [columna[0] for columna in cursor.description]

        fila = cursor.fetchone()

        if fila is None:
            return None

        return dict(zip(columnas, fila))


def agregar_tratamiento_db(
    id_paciente,
    id_medico,
    descripcion,
    fecha_inicio,
    fecha_fin,
    observaciones,
    estado
):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            INSERT INTO tratamientos
            (
                id_paciente,
                id_medico,
                descripcion,
                fecha_inicio,
                fecha_fin,
                observaciones,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            [
                id_paciente,
                id_medico,
                descripcion,
                fecha_inicio,
                fecha_fin,
                observaciones,
                estado
            ]
        )


def actualizar_tratamiento_db(
    id_tratamiento,
    id_paciente,
    id_medico,
    descripcion,
    fecha_inicio,
    fecha_fin,
    observaciones,
    estado
):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            UPDATE tratamientos
            SET
                id_paciente = %s,
                id_medico = %s,
                descripcion = %s,
                fecha_inicio = %s,
                fecha_fin = %s,
                observaciones = %s,
                estado = %s
            WHERE id_tratamiento = %s
            """,
            [
                id_paciente,
                id_medico,
                descripcion,
                fecha_inicio,
                fecha_fin,
                observaciones,
                estado,
                id_tratamiento
            ]
        )