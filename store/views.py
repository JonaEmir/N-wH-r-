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
from .models import Producto, Categoria, Cliente, ContactoCliente, Usuario, Variante, Atributo, AtributoValor, Carrito, CarritoProducto
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


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    tallas = ["3", "4", "5", "6", "7", "8"]

    # lee el origen (dama o caballero), y por seguridad lo validamos
    origen_raw = request.GET.get('from', '')
    origen = origen_raw.lower()
    if origen not in ['dama', 'caballero']:
        origen = 'caballero'  # valor por defecto si viene mal

    return render(
        request,
        'public/detalles.html',
        {
            'producto': producto,
            'origen': origen,
            'tallas': tallas,
        }
    )

@login_required_user
def alta(request):
    return render(request, 'dashboard/registro.html')

def get_categorias(request):
    categorias = Categoria.objects.all().values('id', 'nombre')
    return JsonResponse(list(categorias), safe=False)

@login_required_user
def lista_productos(request):
    return render(request, 'dashboard/lista.html')

@login_required_user
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    categorias = Categoria.objects.all()
    return render(request, 'dashboard/editar.html', {
        'producto': producto,
        'categorias': categorias
    })


@login_required_user          # (opcional, según tu negocio)
@require_GET
def get_all_products(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    productos = Producto.objects.prefetch_related('variantes__attrs__atributo_valor__atributo')
    data = []
    for p in productos:
        variantes = []
        for v in p.variantes.all():
            # recoger los atributos de la variante (talla, color…)
            attrs = {
                attr.atributo_valor.atributo.nombre: attr.atributo_valor.valor
                for attr in v.attrs.all()
            }
            variantes.append({
                'id': v.id,
                'sku': v.sku,
                'precio': float(v.precio or p.precio),
                'stock': v.stock,
                'atributos': attrs,
            })

        data.append({
            'id': p.id,
            'nombre': p.nombre,
            'descripcion': p.descripcion,
            'categoria': p.categoria.nombre,
            'genero': p.genero,
            'en_oferta': p.en_oferta,
            'imagen': p.imagen.url if p.imagen else '',
            'created_at': p.created_at.isoformat(),
            'stock_total': p.stock_total,
            'variantes': variantes,
        })

    return JsonResponse(data, safe=False)

@login_required_user
@require_http_methods(["POST"])
def create_product(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        # ─── Datos básicos del producto ─────────────────────────────
        nombre      = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio      = request.POST['precio']
        categoria   = Categoria.objects.get(id=request.POST['categoria_id'])
        genero      = request.POST['genero']
        en_oferta   = request.POST.get('en_oferta') == 'on'
        imagen      = request.FILES.get('imagen')

        # ─── Arrays de tallas y stocks (si existen) ─────────────────
        tallas = request.POST.getlist('tallas')
        stocks = request.POST.getlist('stocks')

        # Normaliza a ints
        stocks = [int(s) for s in stocks]

    except KeyError as ke:
        return JsonResponse({'error': f'Falta campo {ke}'}, status=400)
    except Categoria.DoesNotExist:
        return JsonResponse({'error': 'Categoría no encontrada'}, status=404)

    # ─── Crea el producto ──────────────────────────────────────────
    producto = Producto.objects.create(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        categoria=categoria,
        genero=genero,
        en_oferta=en_oferta,
        imagen=imagen,
    )

    # ─── Atributo “Talla” (solo se crea/obtiene una vez) ───────────
    atributo_talla, _ = Atributo.objects.get_or_create(nombre='Talla')

    # ────────────────────────────────────────────────────────────────
    # CASO A) Arrays tallas+stocks recibidos y longitudes iguales
    # ────────────────────────────────────────────────────────────────
    if tallas and len(tallas) == len(stocks):
        for talla, stock in zip(tallas, stocks):
            valor_talla, _ = AtributoValor.objects.get_or_create(
                atributo=atributo_talla,
                valor=talla
            )
            variante = Variante.objects.create(
                producto=producto,
                precio=precio,
                stock=stock,
            )
            variante.attrs.create(atributo_valor=valor_talla)

    # ────────────────────────────────────────────────────────────────
    # CASO B) Formulario simple: solo llega “stock” (y opcionalmente “talla”)
    # ────────────────────────────────────────────────────────────────
    else:
        try:
            stock_unico = int(request.POST['stock'])
        except (KeyError, ValueError):
            return JsonResponse({'error': 'Falta campo stock'}, status=400)

        talla_unica = request.POST.get('talla', 'Única')
        valor_talla, _ = AtributoValor.objects.get_or_create(
            atributo=atributo_talla,
            valor=talla_unica
        )
        variante = Variante.objects.create(
            producto=producto,
            precio=precio,
            stock=stock_unico,
        )
        variante.attrs.create(atributo_valor=valor_talla)

    return JsonResponse(
        {'id': producto.id, 'message': 'Producto y variantes creados'}, 
        status=201
    )

@login_required_user
@require_http_methods(["POST"])
def update_productos(request, id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    producto = get_object_or_404(Producto, id=id)

    # Campos del Producto
    for field in ('nombre', 'descripcion', 'precio', 'genero'):
        if field in request.POST:
            setattr(producto, field, request.POST[field])

    if 'en_oferta' in request.POST:
        producto.en_oferta = request.POST.get('en_oferta') == 'on'

    if 'categoria_id' in request.POST:
        try:
            producto.categoria = Categoria.objects.get(id=request.POST['categoria_id'])
        except Categoria.DoesNotExist:
            return JsonResponse({'error': 'Categoría no encontrada'}, status=404)

    if 'imagen' in request.FILES:
        producto.imagen = request.FILES['imagen']

    producto.save()
    return JsonResponse(
        {'mensaje': f'Producto {producto.id} actualizado correctamente'},
        status=200
    )

@login_required_user 
@require_http_methods(["POST"])
def update_variant(request, variante_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    variante = get_object_or_404(Variante, id=variante_id)

    if 'stock' in request.POST:
        variante.stock = int(request.POST['stock'])
    if 'precio' in request.POST:
        variante.precio = request.POST['precio']
    if 'sku' in request.POST:
        variante.sku = request.POST['sku']

    variante.save()
    return JsonResponse(
        {'message': f'Variante {variante.id} actualizada correctamente'},
        status=200
    )

@login_required_user
@require_http_methods(["DELETE"])
def delete_productos(request, id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return JsonResponse({'mensaje': f'Producto {producto.nombre} y sus variantes eliminados'}, status=200)


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

@login_required_user
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
    return redirect("index")


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