from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, dama, caballero, detalle_producto,  login_client, alta, editar_producto, registrarse, get_all_products, create_product, get_categorias, detalle_client, update_variant ,update_productos, delete_productos, lista_productos, get_all_clients, create_client, update_client, delete_client, create_contact, update_contact, create_user, get_user


urlpatterns = [
    #Paths de frontEnd
    #Parte visual del cliente
    path('', index, name='index'),
    path('dama/', dama, name='dama'),
    path('caballero/', caballero, name='caballero'),
    path('registrarse/', registrarse, name='registrarse'),
    path('create-client', create_client),
    path('login-client', login_client, name='login_client'),

    path('producto/<int:id>/', detalle_producto, name='detalle_producto'),

    #Parte visual del admin
    path('dashboard/registro/', alta, name='dashboard_alta'),
    path('dashboard/lista/', lista_productos, name='dashboard_productos'),
    path('dashboard/productos/editar/<int:id>/', editar_producto, name='editar_producto'),



    #Paths de BackEnd
    path('api/productos/', get_all_products, name='get_all_products'),
    path('api/productos/crear/', create_product, name='create_product'),
    path('api/productos/update/<int:id>/', update_productos, name='update_product'),
    path('api/variantes/update/<int:variante_id>/', update_variant, name='update_variant'),
    path('api/productos/delete/<int:id>/', delete_productos, name='delete_product'),
    path('api/categorias/', get_categorias, name='get_categorias'),
    path('clientes', get_all_clients, name="get_all_clients"),
    path('clientes/<int:id>/', detalle_client,  name='detalle_client'),
    path('clientes/crear', create_client, name ="create_client"),
    path('clientes/update/<int:id>', update_client, name ="update_client"),
    path('clientes/delete/<int:id>', delete_client, name ="delete_client"),
    path('contact/create/<int:id>', create_contact, name ="create_contact"),
    path('contact/update/<int:id>', update_contact, name ="update_contact"),
    path('user/get', get_user, name ="get_user"),
    path('user/create', create_user, name ="create_user"),
    #path('user/update/<int:id>', update_user, name ="update_user"),
    #path('user/delete/<int:id>', delete_user, name ="delete_user"),
    path('registro', alta, name='alta')

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
