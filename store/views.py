from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Producto, Categoria
import json

def index(request):
    return render(request, 'public/index.html')

def dama(request):
    return render(request, 'public/dama.html')

def caballero(request):
    return render(request, 'public/caballero.html')

def detalles(request):
    return render(request, 'public/detalles.html')

def alta(request):
    return render(request, 'user/registro.html')

def get_categorias(request):
    categorias = Categoria.objects.all().values('id', 'nombre')
    return JsonResponse(list(categorias), safe=False)



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
            print(producto)
            print(request.POST['nombre'])
            # Accedemos a los campos si están presentes en el request
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
