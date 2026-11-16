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

# roles validos del sistema
NIVELES = ['ADMIN', 'MEDICO', 'RECEPCION', 'VISOR']

def listar_usuarios():
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id_usuario, username, nombre, estado, nivel FROM usuarios ORDER BY username"
        )
        columnas = [col[0] for col in cursor.description]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

def cambiar_nivel(id_usuario, nivel, username_actual):
    # el admin no puede cambiar su propio rol, asi no se queda sin acceso
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE usuarios SET nivel = %s WHERE id_usuario = %s AND username <> %s",
            [nivel, id_usuario, username_actual]
        )