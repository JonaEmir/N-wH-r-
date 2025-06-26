from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_GET
from ..models import Usuario
from .decorators import login_required_user
from django.db.models import Prefetch
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password 
from django.views.decorators.csrf import csrf_exempt
import json


@login_required_user
@require_GET
def get_user(request):
    usuarios = Usuario.objects.all()
    data = []

    for usuario in usuarios:
        data.append({
            'username': usuario.username,
            'role': usuario.role
        })

    return JsonResponse(data, safe=False)

#@login_required_user
@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) #Aqui si se puede parsear el json por que l cabezal es apication json no multipl    
            print(data)
            username = data.get('username')
            password = data.get('password')
            role = data.get('role')

            if not username or not password or not role:
                return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400)
            user = Usuario.objects.create(
                username=username,
                password=make_password(password),
                role=role
            )
            return JsonResponse({'username': user.username, 'message': 'Cliente creado con éxito'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)})

@login_required_user
@require_http_methods(["POST"])
def update_user(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) #Aqui si se puede parsear el json por que l cabezal es apication json no multipl    
            username = data.get('username')
            password = data.get('password')
            user=Usuario.objects.get(id = id)
            if username:
                user.username = username
            if password:
                user.password = make_password(password)
            user.save()
            return JsonResponse({'mensaje':f'user {id} actualizado correctamente'},  status=200)
        except Exception as err:
            return JsonResponse({'error': str(err)})

@login_required_user
@require_http_methods(["DELETE"])
def delete_user(request, id):
    if request.method == 'DELETE':
        try:
            usuario = Usuario.objects.get(id=id)  
            username=usuario.username
            usuario.delete()
            return JsonResponse({'mensaje': f'usuario {username} eliminado correctamente'}, status=200) 
        except usuario.DoesNotExist:
            return JsonResponse({'error': 'usuario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
