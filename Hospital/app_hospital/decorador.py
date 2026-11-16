from functools import wraps
from django.shortcuts import redirect

def roles_permitidos(*roles):
    def decorador(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            nivel = request.session.get('nivel')
            # si no hay sesion iniciada, lo mando al login
            if nivel is None:
                return redirect('login')
            # el admin pasa siempre, los demas solo si su rol esta en la lista
            if nivel != 'ADMIN' and nivel not in roles:
                # NUEVO: en vez de la pantalla blanca, lo mando a la pagina del cartel
                return redirect('no_autorizado')
            return view(request, *args, **kwargs)
        return wrapper
    return decorador

# sin roles en la lista, solo entra el admin
solo_admin = roles_permitidos()