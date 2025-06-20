from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_GET
from ..models import Cliente, ContactoCliente
from .decorators import login_required_user, login_required_client
from django.db.models import Prefetch
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password 
import json


#@login_required_user
@require_GET
def get_all_clients(request):
    if request.method == 'GET':
        clientes = Cliente.objects.all()
        data = []

        for cliente in clientes:
            try:
                contacto = cliente.contactocliente
                data.append({
                    'username': cliente.username,
                    'nombre': contacto.nombre,
                    'email': contacto.email,
                    'mensaje': contacto.mensaje
                })
            except ContactoCliente.DoesNotExist:
                data.append({
                    'username': cliente.username,
                    'nombre': None,
                    'email': None,
                    'mensaje': None
                })

        return JsonResponse(data, safe=False)


@require_http_methods(["POST"])
def create_client(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) #Aqui si se puede parsear el json por que l cabezal es apication json no multipl    
            print(data)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400)
            cliente = Cliente.objects.create(
                username=username,
                password=make_password(password)
            )
            return JsonResponse({'username': cliente.username, 'message': 'Cliente creado con éxito'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)})

@require_http_methods(["POST"])
def update_client(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) #Aqui si se puede parsear el json por que l cabezal es apication json no multipl    
            username = data.get('username')
            password = data.get('password')
            cliente=Cliente.objects.get(id = id)
            if username:
                cliente.username = username
            if password:
                cliente.password = make_password(password)
            cliente.save()
            return JsonResponse({'mensaje':f'Cliente {id} actualizado correctamente'},  status=200)
        except Exception as err:
            return JsonResponse({'error': str(err)})


@require_http_methods(["DELETE"])
def delete_client(request, id):
    if request.method == 'DELETE':
        try:
            cliente = Cliente.objects.get(id=id)  
            username=cliente.nombre
            cliente.delete()
            return JsonResponse({'mensaje': f'cliente {username} eliminado correctamente'}, status=200) 
        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    

def detalle_client(request, id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    # Trae el cliente o devuelve 404
    cliente = get_object_or_404(Cliente, id=id)

    # Intenta cargar el contacto asociado
    try:
        contacto = cliente.contactocliente
        nombre  = contacto.nombre
        email   = contacto.email
        mensaje = contacto.mensaje
    except ContactoCliente.DoesNotExist:
        nombre = email = mensaje = None

    # Responde con JSON
    return JsonResponse({
        'id'      : cliente.id,
        'username': cliente.username,
        'nombre'  : nombre,
        'email'   : email,
        'mensaje' : mensaje,
    }, status=200)


    
@require_http_methods(["POST"])
def create_contact(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) #Aqui si se puede parsear el json por que l cabezal es apication json no multipl    
            print(data)
            cliente = Cliente.objects.get(id=id)  #asigna todo el objeto de clientes con id iual al id del argumento
            nombre = data.get('nombre')
            email = data.get('email')
            mensaje = data.get('mensaje')
            if not nombre or not email or not mensaje:
                return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400)
            contacto = ContactoCliente.objects.create(
                cliente=cliente,
                nombre=nombre,
                email=email,
                mensaje= mensaje
            )
            return JsonResponse({'Contacto ': contacto.nombre, 'message': 'Creado con éxito'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)})

@require_http_methods(["POST"])
def update_contact(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) #Aqui si se puede parsear el json por que l cabezal es apication json no multipl
            nombre = data.get('nombre')
            email = data.get('email')
            mensaje = data.get('mensaje')
            contacto=ContactoCliente.objects.get(cliente__id=id)
            if nombre:
                contacto.nombre = nombre
            if email:
                contacto.email = email
            if mensaje:
                contacto.mensaje = mensaje
            contacto.save()
            return JsonResponse({'mensaje':f'Cliente {id} actualizado correctamente'},  status=200)
        except Exception as err:
            return JsonResponse({'error': str(err)})

