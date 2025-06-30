from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from store.views.decorators import login_required_client
from django.views.decorators.http import require_http_methods
from django.db.models import Sum
from ..models import Cliente, Carrito, Producto, AtributoValor, Variante, CarritoProducto
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(["POST"])
def create_carrito(request, cliente_id):
    try:
        payload = json.loads(request.body)
        prod_id = payload["producto_id"]
        talla_valor = payload["talla"]
        cantidad = int(payload["cantidad"])
    except (json.JSONDecodeError, KeyError, ValueError):
        return JsonResponse({'error': 'JSON inválido o faltan campos'}, status=400)

    cliente = get_object_or_404(Cliente, id=cliente_id)

    carrito, created = Carrito.objects.get_or_create(cliente=cliente, defaults={'status': 'activo'})
    if not created and carrito.status != 'activo':
        carrito.status = 'activo'
        carrito.save(update_fields=['status'])

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

    carrito_prod, creado = CarritoProducto.objects.get_or_create(
        carrito=carrito,
        variante=variante,
        defaults={'cantidad': cantidad}
    )
    if not creado:
        carrito_prod.cantidad += cantidad
        carrito_prod.save(update_fields=['cantidad'])

    subtotal = float((variante.precio if variante.precio else producto.precio) * carrito_prod.cantidad)

    return JsonResponse({
        'mensaje': 'Producto agregado al carrito',
        'carrito_id': carrito.id,
        'status': carrito.status,
        'producto': producto.nombre,
        'variante': {
            'sku': variante.sku,
            'atributos': [str(av) for av in variante.attrs.all()]
        },
        'cantidad': carrito_prod.cantidad,
        'subtotal': subtotal
    }, status=201)


@require_http_methods(["GET"])
def detalle_carrito_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    try:
        carrito = cliente.carrito
    except Carrito.DoesNotExist:
        return JsonResponse({'error': 'El cliente no tiene un carrito.'}, status=404)

    qs = (
        CarritoProducto.objects
        .filter(carrito=carrito)
        .select_related('variante__producto')
        .prefetch_related('variante__attrs__atributo_valor')
    )

    total_piezas = sum(cp.cantidad for cp in qs)
    aplicar_mayoreo = total_piezas >= 6

    items = []
    for cp in qs:
        var = cp.variante
        prod = var.producto

        precio_unit = (
            float(var.precio_mayorista if var.precio_mayorista > 0 else prod.precio_mayorista)
            if aplicar_mayoreo else
            float(var.precio if var.precio else prod.precio)
        )

        items.append({
            'producto':        prod.nombre,
            'precio_unitario': precio_unit,
            'precio_menudeo':  float(var.precio if var.precio else prod.precio),
            'precio_mayorista': float(var.precio_mayorista if var.precio_mayorista > 0 else prod.precio_mayorista),
            'cantidad':        cp.cantidad,
            'atributos':       [str(av) for av in var.attrs.all()],
            'subtotal':        round(precio_unit * cp.cantidad, 2),
            'variante_id':     var.id,
        })

    return JsonResponse({
        'cliente': cliente.username,
        'carrito_id': carrito.id,
        'status': carrito.status,
        'mayoreo': aplicar_mayoreo,
        'items': items,
    }, status=200)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_producto_carrito(request, cliente_id, variante_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    try:
        carrito = cliente.carrito
    except Carrito.DoesNotExist:
        return JsonResponse({'error': 'El cliente no tiene carrito.'}, status=404)

    carrito_prod = get_object_or_404(CarritoProducto, carrito=carrito, variante_id=variante_id)
    carrito_prod.delete()

    return JsonResponse({'mensaje': 'Producto eliminado del carrito.'}, status=200)


@csrf_exempt
@require_http_methods(["DELETE"])
def vaciar_carrito(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    try:
        carrito = cliente.carrito
    except Carrito.DoesNotExist:
        return JsonResponse({'error': 'El cliente no tiene carrito.'}, status=404)

    CarritoProducto.objects.filter(carrito=carrito).delete()
    carrito.status = 'vacio'
    carrito.save(update_fields=['status'])

    return JsonResponse({'mensaje': 'Carrito vaciado.'}, status=200)


@login_required_client
def carrito_cliente(request):
    cliente_id = request.session['cliente_id']
    datos = obtener_productos_del_carrito(cliente_id)
    return render(request, 'public/carrito/carrito.html', {
        'productos': datos['items'],
        'mayoreo': datos['mayoreo'],
    })


def obtener_productos_del_carrito(cliente_id):
    try:
        carrito = Carrito.objects.get(cliente_id=cliente_id)
    except Carrito.DoesNotExist:
        return {'items': [], 'mayoreo': False}

    items = carrito.items.select_related('variante__producto').prefetch_related('variante__attrs__atributo_valor')
    total_piezas = sum(item.cantidad for item in items)
    aplicar_mayoreo = total_piezas >= 6

    productos = []
    for item in items:
        producto = item.variante.producto
        var = item.variante

        precio_unitario = (
            float(var.precio_mayorista if var.precio_mayorista > 0 else producto.precio_mayorista)
            if aplicar_mayoreo else
            float(var.precio if var.precio else producto.precio)
        )

        talla = next(
            (str(attr.atributo_valor.valor) for attr in var.attrs.all()
             if attr.atributo_valor.atributo.nombre.lower() == 'talla'),
            'Única'
        )

        productos.append({
            'nombre': producto.nombre,
            'precio': precio_unitario,
            'cantidad': item.cantidad,
            'talla': talla,
            'imagen': producto.imagen.url if producto.imagen else None,
            'variante_id': var.id,
            'precio_mayorista': float(var.precio_mayorista if var.precio_mayorista > 0 else producto.precio_mayorista),
            'precio_menudeo': float(var.precio if var.precio else producto.precio)
        })

    return {'items': productos, 'mayoreo': aplicar_mayoreo}


@csrf_exempt
@require_http_methods(["PATCH"])
def actualizar_cantidad_producto(request, cliente_id, variante_id):
    try:
        payload = json.loads(request.body)
        cantidad = int(payload["cantidad"])
        if cantidad < 1:
            return JsonResponse({'error': 'Cantidad inválida'}, status=400)
    except (json.JSONDecodeError, KeyError, ValueError):
        return JsonResponse({'error': 'JSON inválido o faltan campos'}, status=400)

    cliente = get_object_or_404(Cliente, id=cliente_id)
    carrito = get_object_or_404(Carrito, cliente=cliente)
    cp = get_object_or_404(CarritoProducto, carrito=carrito, variante_id=variante_id)

    cp.cantidad = cantidad
    cp.save(update_fields=['cantidad'])

    total_piezas = CarritoProducto.objects.filter(carrito=carrito).aggregate(
        total=Sum('cantidad')
    )['total'] or 0

    aplicar_mayoreo = total_piezas >= 6

    items = []
    qs = (
        CarritoProducto.objects
        .filter(carrito=carrito)
        .select_related('variante__producto')
        .prefetch_related('variante__attrs__atributo_valor')
    )

    for item in qs:
        var = item.variante
        prod = var.producto

        precio_unit = (
            float(var.precio_mayorista if var.precio_mayorista > 0 else prod.precio_mayorista)
            if aplicar_mayoreo else
            float(var.precio if var.precio else prod.precio)
        )

        items.append({
            'producto': prod.nombre,
            'precio_unitario': precio_unit,
            'precio_menudeo': float(var.precio if var.precio else prod.precio),
            'precio_mayorista': float(var.precio_mayorista if var.precio_mayorista > 0 else prod.precio_mayorista),
            'cantidad': item.cantidad,
            'atributos': [str(av) for av in var.attrs.all()],
            'subtotal': round(precio_unit * item.cantidad, 2),
            'variante_id': var.id,
        })

    return JsonResponse({
        'cliente': cliente.username,
        'carrito_id': carrito.id,
        'status': carrito.status,
        'mayoreo': aplicar_mayoreo,
        'items': items,
    }, status=200)


@login_required_client
def finalizar_compra(request):
    return render(request, 'public/carrito/finalizar_compra.html')
