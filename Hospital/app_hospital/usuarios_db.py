from django.db import connection

def buscar_usuario(username, password):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id_usuario, username, nombre, nivel FROM usuarios WHERE username = %s AND password = %s",
            [username, password]
        )
        fila = cursor.fetchone()
    # si no encontro nada devuelvo None
    if fila is None:
        return None
    # devuelvo un diccionario para usar user['nivel']
    return {
        'id_usuario': fila[0],
        'username': fila[1],
        'nombre': fila[2],
        'nivel': fila[3],
    }

def existe_usuario(username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE username = %s", [username])
        fila = cursor.fetchone()
    return fila[0] > 0

def crear_usuario(nombre, username, password):
    # todo usuario nuevo se crea como VISOR
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO usuarios (nombre, username, password, estado, nivel) VALUES (%s, %s, %s, 'Activo', 'VISOR')",
            [nombre, username, password]
        )