from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, dama, caballero, detalles, get_all_products, create_product, get_categorias, alta, update_productos, delete_productos, get_all_clients

urlpatterns = [
    path('', index, name='index'),
    path('dama/', dama, name='dama'),
    path('caballero/', caballero, name='caballero'),
    path('detalles/', detalles, name='detalles'),
    path('api/productos/', get_all_products, name='get_all_products'),
    path('api/productos/crear/', create_product, name='create_product'),
    path('api/productos/update/<int:id>/', update_productos, name='update_product'),
    path('api/productos/delete/<int:id>/', delete_productos, name='delete_product'),
    path('api/categorias/', get_categorias, name='get_categorias'),
    path('clientes', get_all_clients, name="get_all_clients"),
    path('registro', alta, name='alta')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
