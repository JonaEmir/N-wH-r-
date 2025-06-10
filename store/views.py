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
                'imagen': p.imagen,
                'stock': p.stock,
                'created_at': p.created_at.isoformat(),
            })
        return JsonResponse(data, safe=False)

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            categoria = Categoria.objects.get(id=body['categoria_id'])

            producto = Producto.objects.create(
                nombre=body['nombre'],
                descripcion=body['descripcion'],
                precio=body['precio'],
                categoria=categoria,
                genero=body['genero'],
                en_oferta=body.get('en_oferta', False),
                imagen=body['imagen'],
                stock=body['stock']
            )
            return JsonResponse({'id': producto.id, 'message': 'Producto creado con éxito'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)