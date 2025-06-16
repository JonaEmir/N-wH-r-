from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Producto, Categoria, Cliente, ContactoCliente, Usuario
import json
from django.contrib.auth.hashers import make_password


def index(request):
    return render(request, 'public/index.html')

def dama(request):
    return render(request, 'public/dama.html')

def caballero(request):
    productos = Producto.objects.filter(genero__iexact='H')
    print('▶︎ Productos caballero:', productos.count())
    return render(request, 'public/caballero.html', {'productos': productos})



def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    # ─── lista de tallas (puedes ajustarla según tu modelo) ───
    tallas = ["3", "4", "5", "6", "7", "8"]

    return render(
        request,
        'public/detalles.html',
        {
            'producto': producto,
            'origen'  : request.GET.get('from', 'caballero'),
            'tallas'  : tallas,                # ← ¡ahora sí la envías!
        }
    )

def alta(request):
    return render(request, 'dashboard/registro.html')

def get_categorias(request):
    categorias = Categoria.objects.all().values('id', 'nombre')
    return JsonResponse(list(categorias), safe=False)

def lista_productos(request):
    return render(request, 'dashboard/lista.html')

from django.shortcuts import get_object_or_404

def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    categorias = Categoria.objects.all()
    return render(request, 'dashboard/editar.html', {
        'producto': producto,
        'categorias': categorias
    })




def get_all_products(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        data = []
        for p in productos:
            data.append({
                'id': p.id,
                'nombre': p.nombre,
                'descripcion': p.descripcion,
                'precio': float(p.precio),
                'categoria': p.categoria.nombre,
                'genero': p.genero,
                'en_oferta': p.en_oferta,
                'stock': p.stock,
                'created_at': p.created_at.isoformat(),
                'imagen': p.imagen.url if p.imagen else '',  # ✅ Asegura que sea una URL válida
            })
        return JsonResponse(data, safe=False)

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        try:
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            precio = request.POST['precio']
            categoria_id = request.POST['categoria_id']
            genero = request.POST['genero']
            en_oferta = request.POST.get('en_oferta') == 'on'  # o puedes hacer bool(int()) si es 0/1
            imagen = request.FILES['imagen']  # <- archivo viene aquí
            stock = request.POST['stock']

            categoria = Categoria.objects.get(id=categoria_id)

            producto = Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                categoria=categoria,
                genero=genero,
                en_oferta=en_oferta,
                imagen=imagen,
                stock=stock
            )
            return JsonResponse({'id': producto.id, 'message': 'Producto creado con éxito'}, status=201)
        except Categoria.DoesNotExist:
            return JsonResponse({'error': 'Categoría no encontrada'}, status=404)
        except KeyError as e:
            return JsonResponse({'error': f'Campo faltante: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def update_productos(request, id):
    if request.method == 'POST':
        try:
            producto = Producto.objects.get(id=id)
            # Accedemos a los campos si están presentes en el request buscar setattr para codigo mas limpio     
            if 'nombre' in request.POST:
                producto.nombre = request.POST['nombre']

            if 'descripcion' in request.POST:
                producto.descripcion = request.POST['descripcion']

            if 'precio' in request.POST:
                producto.precio = request.POST['precio']

            if 'categoria_id' in request.POST:
                categoria = Categoria.objects.get(id=request.POST['categoria_id'])
                producto.categoria = categoria

            if 'genero' in request.POST:
                producto.genero = request.POST['genero']

            if 'en_oferta' in request.POST:
                producto.en_oferta = request.POST.get('en_oferta') == 'on'

            if 'stock' in request.POST:
                producto.stock = request.POST['stock']

            if 'imagen' in request.FILES:
                producto.imagen = request.FILES['imagen']

            producto.save()
            return JsonResponse({'mensaje': f'Producto {producto.nombre} actualizado correctamente'}, status=200)

        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
        except Categoria.DoesNotExist:
            return JsonResponse({'error': 'Categoría no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def delete_productos(request, id):
    if request.method == 'DELETE':
        try:
            producto = Producto.objects.get(id=id)  
            nombre=producto.nombre
            producto.delete()
            return JsonResponse({'mensaje': f'Producto {nombre} eliminado correctamente'}, status=200)
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



def get_all_clients(request):
    if request.method == 'GET':
        clientes = Cliente.objects.all()
        data = []

        for cliente in clientes:
            try:
                contacto = cliente.contactocliente  # accede al contacto relacionado
                data.append({
                    'username': cliente.username,
                    'password': cliente.password,
                    'nombre': contacto.nombre,
                    'email': contacto.email,
                    'mensaje': contacto.mensaje
                })
            except ContactoCliente.DoesNotExist:
                # Si el cliente no tiene contacto asociado
                data.append({
                    'username': cliente.username,
                    'password': cliente.password,
                    'nombre': None,
                    'email': None,
                    'mensaje': None
                })

        return JsonResponse(data, safe=False)


@csrf_exempt
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
    
@csrf_exempt
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

@csrf_exempt
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
    

@csrf_exempt
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
    
@csrf_exempt
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




def get_user(request):
    if request.method == 'GET':
        usuarios = Usuario.objects.all()
        data = []

        for usuario in usuarios:
            try:
                data.append({
                    'username': usuario.username,
                    'password': usuario.password,
                    'role' : usuario.role
                })
            except Exception as e:
                # Si el cliente no tiene contacto asociado
                return JsonResponse({'error': str(e)})

        return JsonResponse(data, safe=False)


@csrf_exempt
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
    
@csrf_exempt
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

@csrf_exempt
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
    

