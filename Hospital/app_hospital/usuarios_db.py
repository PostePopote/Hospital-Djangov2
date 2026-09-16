from django.db import connection


def obtener_usuario(username, password):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT *
            FROM usuarios
            WHERE username = %s
            AND password = %s
            """,
            [username, password]
        )

        columnas = [columna[0] for columna in cursor.description]

        fila = cursor.fetchone()

        if fila is None:
            return None

        return dict(zip(columnas, fila))