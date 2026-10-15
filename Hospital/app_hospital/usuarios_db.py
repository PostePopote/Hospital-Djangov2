from django.db import connection


def obtener_usuario(username, password):
    # Busca en la base de datos un usuario con las credenciales proporcionadas.

    with connection.cursor() as cursor:

        # Ejecuta la consulta con parámetros para mantener los valores seguros.
        cursor.execute(
            """
            SELECT *
            FROM usuarios
            WHERE username = %s
            AND password = %s
            """,
            [username, password]
        )

        # Recupera los nombres de las columnas y la primera fila coincidente.
        columnas = [columna[0] for columna in cursor.description]

        fila = cursor.fetchone()

        # Si no hay coincidencias, indica que el usuario no existe.
        if fila is None:
            return None

        # Combina los nombres de columna y sus valores en un diccionario.
        return dict(zip(columnas, fila))