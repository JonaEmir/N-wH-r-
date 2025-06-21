import json
import logging
from django.shortcuts import get_object_or_404
from django.http      import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ..models import Cliente, Wishlist, Producto

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(['GET','PATCH', 'DELETE'])
def wishlist_detail(request, id_cliente):
    cliente, _  = Cliente.objects.get_or_create(id=id_cliente)
    wishlist, _ = Wishlist.objects.get_or_create(cliente=cliente)

    if request.method == 'GET':
        ids = list(wishlist.productos.values_list('id', flat=True))
        return JsonResponse({'productos': ids})

    # PATCH

    try:
        payload = json.loads(request.body)
        prod_id  = payload['producto_id']
    except (json.JSONDecodeError, KeyError) as e:
        print(f"[Wishlist] JSON inválido: {e}")      # aparece en consola
        return JsonResponse({'error': 'JSON inválido o falta "producto_id"'}, status=400)

    # Intentamos obtener el producto, pero sin get_object_or_404
    try:
        producto = Producto.objects.get(pk=prod_id)
    except Producto.DoesNotExist:
        # Esto sale en tu terminal/console donde corre runserver
        print(f"[Wishlist] Producto no encontrado: id={prod_id}")
        # y opcionalmente también con logging:
        logger.error(f"Intento de añadir producto inexistente id={prod_id} en wishlist {wishlist.id}")
        return JsonResponse({'error': f'No existe Producto con id={prod_id}'}, status=404)   

    if request.method == 'PATCH':
        if wishlist.productos.filter(pk=producto.pk).exists():
            return JsonResponse(
                {'error': 'Producto ya agregado a la wishlist'},
                status=400
            )
        
        wishlist.productos.add(producto)
        ids = list(wishlist.productos.values_list('id', flat=True))
        return JsonResponse({'productos': ids})
    elif request.method=='DELETE':
        wishlist.productos.remove(producto)
        ids = list(wishlist.productos.values_list('id', flat=True))
        return JsonResponse({'productos': ids})




@csrf_exempt
@require_http_methods([ 'DELETE'])
def wishlist_all(request, id_cliente):
    cliente, _  = Cliente.objects.get_or_create(id=id_cliente)
    wishlist, _ = Wishlist.objects.get_or_create(cliente=cliente)
    wishlist.productos.clear()
    return JsonResponse({'mensaje': 'productos eliminados correctamente'})
