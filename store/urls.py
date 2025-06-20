from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views.views import detalle_carrito, create_carrito, update_carrito, delete_carrito, index, genero_view, login_user, logout_user, logout_client,  login_client, alta, editar_producto, registrarse, get_categorias, detalle_client, lista_productos, get_all_clients, create_client, update_client, delete_client, create_contact, update_contact, create_user, get_user, delete_user, update_user
from .views.products import get_all_products, delete_productos, update_productos, create_product, update_variant, detalle_producto

urlpatterns = [
    #Paths de frontEnd
    #Parte visual del cliente
    path('', index, name='index'),
    path('coleccion/<str:genero>/', genero_view, name='coleccion_genero'),
    path('registrarse/', registrarse, name='registrarse'),
    path('logout-client', logout_client, name="logout_client"),


    path('create-client', create_client),
    path('login-client', login_client, name='login_client'),

    

    #Parte visual del admin
    path('dashboard/login/', login_user, name='login_user'),
    path('dashboard/logout/', logout_user, name='logout_user')  # ✅ más claro y consistente
,


    path('dashboard/registro/', alta, name='dashboard_alta'),
    path('dashboard/lista/', lista_productos, name='dashboard_productos'),
    path('dashboard/productos/editar/<int:id>/', editar_producto, name='editar_producto'),



    #Paths de BackEnd
    path('producto/<int:id>/', detalle_producto, name='detalle_producto'),
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
    path('user/update/<int:id>', update_user, name ="update_user"),
    path('user/delete/<int:id>', delete_user, name ="delete_user"),
    #Paths carrito
    path('carrito/<int:id>/', detalle_carrito,  name='detalle_carrito'),
    path('carrito/crear', create_carrito, name ="create_carrito"),
    path('carrito/update/<int:id>', update_carrito, name ="update_carrito,delete_carrito"),
    path('carrito/delete/<int:id>', delete_carrito, name ="delete_carrito"),

    path('registro', alta, name='alta')

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
