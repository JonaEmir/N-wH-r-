from django.shortcuts import render, get_object_or_404

# 
"""
    get_object_or_404 

    si el objeto existe en la base de datos te lo devuelve; si no existe, 
    lanza automáticamente un error 404 y tu vista detiene la ejecución 
    mostrando la página de “No encontrado”.

    Esta linea :

        producto = get_object_or_404(Producto, id=id)

    Internamente hace esto:
        try:
            obj = Producto.objects.get(id=id)
        except Producto.DoesNotExist:
            raise Http404("No existe ese Producto")
        return obj

"""
from django.http import JsonResponse
from ..models import Producto, Categoria, Cliente, ContactoCliente, Usuario, Variante, Atributo, AtributoValor, Carrito, CarritoProducto
import json
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password 
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf   import csrf_exempt

from django.db.models import Prefetch
from random import sample
from django.http import HttpResponseNotFound
from django.shortcuts import redirect

#Importaciones para manejar con seguridad que cualquier usuario no identificado o mal identificado acceda a rutas que no debe
from functools import wraps



#Evitar que un usuario no autenticado acceda a rutas privadas (como el dashboard).
#Mostrar contenido distinto si el cliente ya inició sesión.
#Permitir cerrar sesión limpiamente.

def login_required_client(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("cliente_id"):
            return redirect("index")
        return view_func(request, *args, **kwargs)
    return wrapper

def login_required_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("login_user")

        # Validar que el usuario tenga rol 'admin'
        try:
            user = Usuario.objects.get(id=user_id)
            if user.role != "admin":
                return redirect("login_user")
        except Usuario.DoesNotExist:
            return redirect("login_user")

        return view_func(request, *args, **kwargs)
    return wrapper



#Estamos creando y declarando las rutas para el inicio de sesion del Administrador
@require_http_methods(["GET", "POST"])
def login_user(request):
    if request.method == "GET":
        return render(request, "dashboard/login.html")

    # POST
    username = request.POST.get("username")
    password = request.POST.get("password")

    if not username or not password:
        return render(request, "dashboard/login.html", {"error": "Campos obligatorios"})

    try:
        user = Usuario.objects.get(username=username)
        if not check_password(password, user.password):
            raise ValueError("Contraseña incorrecta")
    except Exception:
        return render(request, "dashboard/login.html", {"error": "Credenciales inválidas"})

    request.session["user_id"] = user.id
    request.session["user_username"] = user.username
    return redirect("dashboard_productos")



#Muestra en index.html 4 productos de cada seccion, para dama y para mujer
def index(request):
    # Query base: un producto por fila
    qs_h = Producto.objects.filter(
        genero__iexact='H',
        variantes__stock__gt=0
    ).distinct().prefetch_related(
        Prefetch('variantes', Variante.objects.all())
    )

    qs_m = Producto.objects.filter(
        genero__iexact='M',
        variantes__stock__gt=0
    ).distinct().prefetch_related(
        Prefetch('variantes', Variante.objects.all())
    )

    # Elegimos 4 aleatorios sin repetir
    cab_home  = sample(list(qs_h), min(4, qs_h.count()))
    dama_home = sample(list(qs_m), min(4, qs_m.count()))

    return render(request, 'public/index.html', {
        'cab_home': cab_home,
        'dama_home': dama_home,
    })



def registrarse(request):
    if request.session.get("cliente_id"):
        return redirect("index")
    return render(request, "public/registro-usuario.html")

@login_required_user
def alta(request):
    return render(request, 'dashboard/registro.html')

def get_categorias(request):
    categorias = Categoria.objects.all().values('id', 'nombre')
    return JsonResponse(list(categorias), safe=False)

@login_required_user
def lista_productos(request):
    return render(request, 'dashboard/lista.html')

#vista del cliente no es funcion logica
@login_required_user
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    categorias = Categoria.objects.all()

    variantes = producto.variantes.select_related().prefetch_related('attrs__atributo_valor')

    # Serializa las variantes para el template
    variantes_data = []
    for v in variantes:
        talla = None
        for av in v.attrs.all():
            if av.atributo_valor.atributo.nombre.lower() == "talla":
                talla = av.atributo_valor.valor
                break
        variantes_data.append({
            'id': v.id,
            'talla': talla or '—',
            'precio': v.precio,
            'stock': v.stock,
        })

    return render(request, 'dashboard/editar.html', {
        'producto': producto,
        'categorias': categorias,
        'variantes': variantes_data,
    })

@require_POST          # fuerza solo POSTAdd commentMore actions
def login_client(request):
    """
    Comprueba usuario y contraseña de Cliente.
    Devuelve:
      200 OK  → éxito
      404     → usuario no registrado
      401     → contraseña incorrecta
    """
    import json
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"error": "Faltan campos"}, status=400)

        try:
            cliente = Cliente.objects.get(username=username)
        except Cliente.DoesNotExist:
            return JsonResponse({"error": "Usuario no registrado"}, status=404)

        if not check_password(password, cliente.password):
            return JsonResponse({"error": "Campos incorrectos"}, status=401)

        # marcar sesión (opcional pero recomendado)
        request.session["cliente_id"] = cliente.id
        request.session["cliente_username"] = cliente.username

        return JsonResponse({"message": "Inicio de sesión exitoso"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
def genero_view(request, genero):  # genero = 'dama' o 'caballero'
    genero_map = {
        'dama': 'M',
        'caballero': 'H',
    }

    genero_codigo = genero_map.get(genero.lower())
    if not genero_codigo:
        return HttpResponseNotFound("Género no válido")

    qs = Producto.objects.filter(
        genero__iexact=genero_codigo,
        variantes__stock__gt=0
    ).select_related('categoria').distinct()

    categorias = sorted({p.categoria.nombre for p in qs})

    return render(
        request,
        'public/productos_genero.html',
        {
            'seccion'   : genero,
            'titulo'    : 'Mujer' if genero == 'dama' else 'Hombre',
            'categorias': categorias,
            'productos' : qs,
        }
    )

@require_http_methods(["POST"])
def logout_client(request):
    request.session.flush()  # elimina todos los datos de sesión
    return redirect('index')  # redirige al home

def logout_user(request):
    request.session.flush()
    return redirect("login_user")  # ✅ redirige al login del dashboard



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