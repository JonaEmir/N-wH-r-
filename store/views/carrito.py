from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from ..models import Cliente, Carrito, Producto, AtributoValor, Variante, CarritoProducto
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(["POST"])
def create_carrito(request, cliente_id):
    # 1) Parsear y validar JSON
    try:
        payload     = json.loads(request.body)
        prod_id     = payload["producto_id"]
        talla_valor = payload["talla"]
        cantidad    = int(payload["cantidad"])
    except (json.JSONDecodeError, KeyError, ValueError):
        return JsonResponse({'error': 'JSON inválido o faltan campos'}, status=400)

    # 2) Obtener cliente
    cliente = get_object_or_404(Cliente, id=cliente_id)

    # 3) Obtener o crear/activar carrito “activo”
    carrito, created = Carrito.objects.get_or_create(
        cliente=cliente,
        defaults={'status': 'activo'}
    )
    if not created and carrito.status != 'activo':
        carrito.status = 'activo'
        carrito.save(update_fields=['status'])

    # 4) Resolver Variante
    producto = get_object_or_404(Producto, id=prod_id)
    atributo_valor = get_object_or_404(
        AtributoValor,
        atributo__nombre="Talla",
        valor=talla_valor
    )


    variante = get_object_or_404(
        Variante.objects.prefetch_related('attrs'),
        producto=producto,
        attrs__atributo_valor=atributo_valor
    )

    # 5) Añadir o actualizar cantidad
    carrito_prod, creado = CarritoProducto.objects.get_or_create(
        carrito=carrito,
        variante=variante,
        defaults={'cantidad': cantidad}
    )
    if not creado:
        carrito_prod.cantidad += cantidad
        carrito_prod.save(update_fields=['cantidad'])

    # 6) Responder
    return JsonResponse({
        'mensaje':    'Producto agregado al carrito',
        'carrito_id': carrito.id,
        'status':     carrito.status,
        'producto':   producto.nombre,
        'variante': {
            'sku':       variante.sku,
            'atributos': [ str(av) for av in variante.attrs.all() ]
        },
        'cantidad':   carrito_prod.cantidad,
        # opcional: subtotal aquí en back
        'subtotal':   float((variante.precio or producto.precio) * carrito_prod.cantidad)
    }, status=201)


@require_http_methods(["GET"])
def detalle_carrito_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    try:
        carrito = cliente.carrito
    except Carrito.DoesNotExist:
        return JsonResponse({'error': 'El cliente no tiene un carrito.'}, status=404)

    items = []
    qs = (
        CarritoProducto.objects
        .filter(carrito=carrito)
        .select_related('variante__producto')
        .prefetch_related('variante__attrs__atributo_valor')
    )

    for cp in qs:
        var  = cp.variante
        prod = var.producto
        precio_unit = float(var.precio or prod.precio)
        items.append({
            'producto':        prod.nombre,
            'precio_unitario': precio_unit,
            'cantidad':        cp.cantidad,
            'atributos':       [ str(av) for av in var.attrs.all() ],
            'subtotal':        round(precio_unit * cp.cantidad, 2),
        })

    return JsonResponse({
        'cliente':    cliente.username,
        'carrito_id': carrito.id,
        'status':     carrito.status,
        'items':      items,
    }, status=200)



@csrf_exempt
@require_http_methods(["DELETE"])
def delete_producto_carrito(request, cliente_id, variante_id):
    """
    Elimina una variante concreta del carrito activo del cliente.
    """
    # 1) Cliente → carrito
    cliente = get_object_or_404(Cliente, id=cliente_id)
    try:
        carrito = cliente.carrito
    except Carrito.DoesNotExist:
        return JsonResponse({'error': 'El cliente no tiene carrito.'}, status=404)

    # 2) Buscar y borrar la línea de CarritoProducto
    carrito_prod = get_object_or_404(
        CarritoProducto,
        carrito=carrito,
        variante_id=variante_id
    )
    carrito_prod.delete()

    return JsonResponse(
        {'mensaje': 'Producto eliminado del carrito.'},
        status=200
    )


@csrf_exempt
@require_http_methods(["DELETE"])
def vaciar_carrito(request, cliente_id):
    """
    Elimina todos los items del carrito activo del cliente y lo marca como 'vacio'.
    """
    # 1) Cliente → carrito
    cliente = get_object_or_404(Cliente, id=cliente_id)
    try:
        carrito = cliente.carrito
    except Carrito.DoesNotExist:
        return JsonResponse({'error': 'El cliente no tiene carrito.'}, status=404)

    # 2) Borrar todos los CarritoProducto
    CarritoProducto.objects.filter(carrito=carrito).delete()

    # 3) Marcar el carrito como vacío
    carrito.status = 'vacio'
    carrito.save(update_fields=['status'])

    return JsonResponse(
        {'mensaje': 'Carrito vaciado.'},
        status=200
    )