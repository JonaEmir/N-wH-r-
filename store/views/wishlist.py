import json
import logging
import decimal

from django.shortcuts import get_object_or_404, render, redirect
from django.http      import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http  import require_http_methods

from ..models import Cliente, Wishlist, Producto, VarianteAtributo

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(['GET'])
def get_cliente_id(request, username):
    """
    GET /api/cliente_id/<username>/
    Devuelve {"id": <cliente.id>} o 404 si no existe.
    """
    cliente = get_object_or_404(Cliente, username=username)
    return JsonResponse({'id': cliente.id})
# ---------------------------------------------------------------------------
@csrf_exempt
@require_http_methods(['GET', 'PATCH', 'DELETE'])
def wishlist_detail(request, id_cliente):
    cliente, _  = Cliente.objects.get_or_create(id=id_cliente)
    wishlist, _ = Wishlist.objects.get_or_create(cliente=cliente)

    # ───── GET: devuelve sólo la lista de IDs ───────────────────────────────
    if request.method == 'GET':
        """ producto = get_object_or_404(Producto, pk=id)   # 2️⃣  usa la misma variable

        precio = float(producto.precio) if isinstance(producto.precio, decimal.Decimal) else producto.precio

        data = {
                "id":     producto.id,
                "nombre": producto.nombre,
                "precio": precio,
                "imagen": request.build_absolute_uri(producto.imagen.url) if producto.imagen else "",
            }
        return JsonResponse(data)"""
        productos=[]
        ids = list(wishlist.productos.values_list('id', flat=True))
        for i in ids:
            producto = get_object_or_404(Producto, id=i)
            if producto.imagen:
                imagen_url = request.build_absolute_uri(producto.imagen.url)
            else:
                imagen_url = None
            
            productos.append({
                "id": i,
                "nombre": producto.nombre,
                "precio": producto.precio,
                "imagen": imagen_url
            })

        return JsonResponse({'productos': productos})

    # ───── PATCH / DELETE: cuerpo JSON con "producto_id" ────────────────────
    try:
        payload = json.loads(request.body)
        prod_id = payload['producto_id']
    except (json.JSONDecodeError, KeyError) as e:
        print(f"[Wishlist] JSON inválido: {e}")
        return JsonResponse({'error': 'JSON inválido o falta "producto_id"'}, status=400)

    try:
        producto = Producto.objects.get(pk=prod_id)
    except Producto.DoesNotExist:
        print(f"[Wishlist] Producto no encontrado: id={prod_id}")
        logger.error(f"Intento de añadir producto inexistente id={prod_id} en wishlist {wishlist.id}")
        return JsonResponse({'error': f'No existe Producto con id={prod_id}'}, status=404)

    if request.method == 'PATCH':
        if wishlist.productos.filter(pk=producto.pk).exists():
            return JsonResponse({'error': 'Producto ya agregado a la wishlist'}, status=400)

        wishlist.productos.add(producto)

    elif request.method == 'DELETE':
        wishlist.productos.remove(producto)

    ids = list(wishlist.productos.values_list('id', flat=True))
    return JsonResponse({'productos': ids})


# ---------------------------------------------------------------------------
@csrf_exempt
@require_http_methods(['DELETE'])
def wishlist_all(request, id_cliente):
    cliente, _  = Cliente.objects.get_or_create(id=id_cliente)
    wishlist, _ = Wishlist.objects.get_or_create(cliente=cliente)
    wishlist.productos.clear()
    return JsonResponse({'mensaje': 'productos eliminados correctamente'})


@csrf_exempt
@require_http_methods(['GET'])
def producto_tallas(request, id_producto):
    """
    GET /api/productos/<id_producto>/
    Devuelve {"tallas": ["24","25",...]} ó ["Única"] si no hay atributo “Talla”.
    """
    producto = Producto.objects.filter(pk=id_producto).first()
    if not producto:
        raise Http404("Producto no encontrado")

    # 1) Obtenemos todas las tallas distintas de variantes con stock>0
    tallas_qs = (VarianteAtributo.objects
        .filter(
            variante__producto   = producto,
            variante__stock__gt  = 0,
            atributo_valor__atributo__nombre__iexact = "talla"   # clave
        )
        .values_list("atributo_valor__valor", flat=True)
        .distinct()
    )

    tallas = sorted(tallas_qs) or ["Única"]
    return JsonResponse({"tallas": tallas})