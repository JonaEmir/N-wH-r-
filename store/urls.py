from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, dama, caballero, detalle_producto, alta, editar_producto, get_all_products, create_product, get_categorias, update_productos, delete_productos, lista_productos, get_all_clients, create_client, update_client, delete_client, create_contact, update_contact


urlpatterns = [
    #Paths de frontEnd
    #Parte visual del cliente
    path('', index, name='index'),
    path('dama/', dama, name='dama'),
    path('caballero/', caballero, name='caballero'),

    path('producto/<int:id>/', detalle_producto, name='detalle_producto'),

    #Parte visual del admin
    path('dashboard/registro/', alta, name='dashboard_alta'),
    path('dashboard/lista/', lista_productos, name='dashboard_productos'),
    path('dashboard/productos/editar/<int:id>/', editar_producto, name='editar_producto'),



    #Paths de BackEnd
    path('api/productos/', get_all_products, name='get_all_products'),
    path('api/productos/crear/', create_product, name='create_product'),
    path('api/productos/update/<int:id>/', update_productos, name='update_product'),
    path('api/productos/delete/<int:id>/', delete_productos, name='delete_product'),
    path('api/categorias/', get_categorias, name='get_categorias'),
    path('clientes', get_all_clients, name="get_all_clients"),
    path('clientes/crear', create_client, name ="create_client"),
    path('clientes/update/<int:id>', update_client, name ="update_client"),
    path('clientes/delete/<int:id>', delete_client, name ="delete_client"),
    path('contact/create/<int:id>', create_contact, name ="create_contact"),
    path('contact/update/<int:id>', update_contact, name ="update_contact"),
    path('registro', alta, name='alta')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
