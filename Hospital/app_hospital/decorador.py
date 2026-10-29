from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def solo_admin(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        # si no hay sesion iniciada, lo mando al login
        if 'nivel' not in request.session:
            return redirect('login')
        # si no es admin, no lo dejo pasar
        if request.session.get('nivel') != 'ADMIN':
            return HttpResponseForbidden('No autorizado')
        return view(request, *args, **kwargs)
    return wrapper