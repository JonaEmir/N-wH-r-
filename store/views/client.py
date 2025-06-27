from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_GET
from ..models import Cliente, ContactoCliente
from .decorators import login_required_user, login_required_client
from django.db.models import Prefetch
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password 
import json
from django.views.decorators.csrf import csrf_exempt


"""
get_all_clients devuelve la lista completa de clientes registrados
"""
#@login_required_user
@require_GET
def get_all_clients(request):
    if request.method == 'GET':
        clientes = Cliente.objects.all()
        data = []

        for cliente in clientes:
            try:
                data.append({
                    'id': cliente.id,
                    'username': cliente.username,
                    'nombre': cliente.nombre,
                    'email': cliente.correo,
                })
            except Exception as e:
                return JsonResponse({"mensaje": str(e)})

        return JsonResponse(data, safe=False)



"""
-detalle_client devuelve la informacion de un cliente en especifico por id
"""
def detalle_client(request, id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    # Trae el cliente o devuelve 404
    cliente = get_object_or_404(Cliente, id=id)

    # Intenta cargar el contacto asociado
    try:
        nombre  = cliente.nombre
        email   = cliente.correo
        telefono = cliente.telefono
        direccion = cliente.direccion
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    # Responde con JSON
    return JsonResponse({
        'id'      : cliente.id,
        'username': cliente.username,
        'nombre'  : nombre,
        'email'   : email,
        'telefono' : telefono,
        'direccion': direccion
    }, status=200)


   

"""
-create_client registra un nuevo cliente 
-campos obligatorios: username, password y correo
"""
@csrf_exempt
@require_http_methods(["POST"])
def create_client(request):
    try:
        data = json.loads(request.body)
        print("📥 Datos recibidos:", data)

        username  = data.get('username')
        password  = data.get('password')
        correo    = data.get('correo')
        nombre    = data.get('nombre')
        telefono  = data.get('telefono')
        direccion = data.get('direccion')

        # Validación de campos obligatorios
        if not username or not password or not correo:
            return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400)

        cliente = Cliente.objects.create(
            username=username,
            password=make_password(password),
            correo=correo,
            nombre=nombre,
            telefono=telefono,
            direccion=direccion
        )

        print("✅ Cliente creado con ID:", cliente.id)
        return JsonResponse({'username': cliente.username, 'message': 'Cliente creado con éxito'}, status=201)

    except Exception as e:
        print("❌ Error al crear cliente:", str(e))
        return JsonResponse({'error': str(e)}, status=400)




"""
-update_client edita o actiualiza el registro del cliente.
-Ningun campo es obligatorio, puedes actualizar cualquier campo individualmente 
"""
@csrf_exempt
@require_http_methods(["POST"])
def update_client(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) #Aqui si se puede parsear el json por que l cabezal es apication json no multipl    
            username = data.get('username')
            password = data.get('password')
            correo = data.get('correo')
            nombre = data.get('nombre')
            telefono = data.get('telefono')
            direccion = data.get('direccion')
            cliente=Cliente.objects.get(id = id)
            if username:
                cliente.username = username
            if password:
                cliente.password = make_password(password)
            if correo:
                cliente.correo=correo
            if nombre:
                cliente.nombre=nombre
            if telefono:
                cliente.telefono=telefono
            if direccion:
                cliente.direccion=direccion
            cliente.save()
            return JsonResponse({'mensaje':f'Cliente {id} actualizado correctamente'},  status=200)
        except Exception as err:
            return JsonResponse({'error': str(err)})

"""
-delete_client elimina un cliente en especifico por id
"""
@require_http_methods(["POST", "DELETE"])
def delete_client(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
        username = cliente.nombre
        cliente.delete()

        # Si es un formulario HTML (POST), redirige al dashboard
        if request.method == "POST":
            return redirect('dashboard_clientes')

        # Si es una llamada AJAX DELETE
        return JsonResponse({'mensaje': f'Cliente {username} eliminado correctamente'}, status=200)

    except Cliente.DoesNotExist:
        if request.method == "POST":
            return redirect('dashboard_clientes')
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

    except Exception as e:
        if request.method == "POST":
            return redirect('dashboard_clientes')
        return JsonResponse({'error': str(e)}, status=400)   
 


"""
Funciones de contacto para que el cliente se comunique por correo con nosotros 
Todos los campos obligatorios
"""
@require_http_methods(["POST"])
def send_contact(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) #Aqui si se puede parsear el json por que l cabezal es apication json no multipl    
            cliente = Cliente.objects.get(id=id)  #asigna todo el objeto de clientes con id iual al id del argumento
            email = data.get('email')
            mensaje = data.get('mensaje')
            
            if not mensaje or not email :
                return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400)
            contacto = ContactoCliente.objects.create(
                cliente=cliente,
                email=email,
                mensaje=mensaje
            )
            return JsonResponse({'Contacto ': contacto.nombre, 'message': 'Creado con éxito'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)})
