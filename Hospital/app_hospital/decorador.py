
from functools import wraps
from django.shortcuts import redirect

def solo_admin(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):

        # Si no hay una sesión iniciada, lo manda al login
        if 'nivel' not in request.session:
            return redirect('login')

        # Si no es administrador, muestra la alerta
        if request.session.get('nivel') != 'ADMIN':
            return redirect('no_autorizado')

        # Si es administrador, permite acceder
        return view(request, *args, **kwargs)

    return wrapper
