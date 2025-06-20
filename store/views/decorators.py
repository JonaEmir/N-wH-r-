# store/views/decorators.py

from functools import wraps
from django.shortcuts import redirect
from ..models import Usuario

def login_required_client(view_func):
    """
    Asegura que haya un cliente logueado en sesión.
    Si no, redirige al home público.
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get("cliente_id"):
            return redirect("index")
        return view_func(request, *args, **kwargs)
    return _wrapped

def login_required_user(view_func):
    """
    Asegura que haya un usuario admin logueado en sesión.
    Si no existe sesión o el rol no es 'admin', redirige al login de dashboard.
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("login_user")

        try:
            user = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            return redirect("login_user")

        if user.role != "admin":
            return redirect("login_user")

        return view_func(request, *args, **kwargs)
    return _wrapped
