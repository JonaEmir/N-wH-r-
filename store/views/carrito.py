from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_GET
from ..models import Carrito, CarritoProducto 
from .decorators import login_required_user, login_required_client
from django.db.models import Prefetch
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password 
from django.views.decorators.csrf import csrf_exempt
import json



def detalle_carrito(request, id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    carrito = get_object_or_404(Carrito, id=id)
    cliente = carrito.cliente

    # 1) Todas las relaciones CarritoProducto para este carrito
    items = CarritoProducto.objects.filter(carrito=carrito)
    # — o bien —
    items = carrito.carritoproducto_set.all()

    # Ahora construimos la respuesta (JSON de ejemplo)
    data = []
    for cp in items.select_related('variante__producto'):
        var = cp.variante
        prod = var.producto
        # Lista de atributos (talla, color…) si los tienes
        attrs = [str(av) for av in var.attrs.all()]
        data.append({
            'producto': prod.nombre,
            'precio_unitario': float(var.precio or prod.precio),
            'atributos': attrs,
        })

    return JsonResponse({
        'cliente': cliente.username,
        'items': data,
    })

@csrf_exempt  # si lo llamas desde JS asegúrate de enviar X-CSRFToken o eximirlo
@require_http_methods(["POST"])
def create_carrito(request, cliente_id):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    cliente = get_object_or_404(Cliente, id=cliente_id)
    if hasattr(cliente, 'carrito'):
        return JsonResponse({'error': 'El cliente ya tiene un carrito.'}, status=400)
    status = payload.get('status', 'vacio')
    carrito = Carrito.objects.create(cliente=cliente, status=status)
    return JsonResponse({
        'id':          carrito.id,
        'cliente':     cliente.username,
        'status':      carrito.status,
        'created_at':  carrito.created_at.isoformat(),
    }, status=201)

@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def update_carrito(request, id):
    # 1) Parsear JSON
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    # 2) Obtener carrito o 404
    carrito = get_object_or_404(Carrito, id=id)

    # 3) Campos que permitimos cambiar
    campos_posibles = {
        'status':        lambda val: setattr(carrito, 'status', val),
        'cliente_id':    lambda val: setattr(carrito, 'cliente', get_object_or_404(Cliente, id=val)),
    }

    # 4) Aplicar sólo los que vienen en payload
    campos_actualizados = []
    for campo, setter in campos_posibles.items():
        if campo in payload:
            setter(payload[campo])
            # en el modelo el field se llama “cliente” pero lo pasamos como “cliente_id”
            campos_actualizados.append('cliente' if campo=='cliente_id' else campo)

    if not campos_actualizados:
        return JsonResponse({'error': 'No se enviaron campos a actualizar.'}, status=400)

    # 5) Guardar sólo los update_fields necesarios
    carrito.save(update_fields=campos_actualizados)
    return JsonResponse({
        'mensaje':    'Carrito actualizado',
        'id':         carrito.id,
        'status':     carrito.status,
        'cliente':    carrito.cliente.username,
    }, status=200)


def delete_carrito(request,id):

    if request.method != 'DELETE':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    carrito = get_object_or_404(Carrito, id=id)
    carrito.delete()
    return JsonResponse({'mensaje': f'carrito {carrito.id}  eliminados'}, status=200)

