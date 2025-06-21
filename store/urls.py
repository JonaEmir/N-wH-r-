# store/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


#prueba para acceder a recuperar contrasena
from .views.reset_password import solicitar_reset

#acomodar todo esto 
from .views.reset_password import (
    solicitar_reset,
    reset_password_confirm,
    reset_password_submit,
)



# ────────── Vistas que SIGUEN en views/views.py ──────────
from .views.views import (
    # Home y secciones públicas
    index, genero_view, registrarse,
    # Dashboard básicos
    alta, lista_productos, editar_producto,
    # Auxiliares
    get_categorias,
    # Autenticación (admin y cliente)
    login_user, logout_user,
    login_client, logout_client,
)

# ────────── Carrito (views/carrito.py) ──────────
from .views.carrito import (
    detalle_carrito, create_carrito,
    update_carrito, delete_carrito,
)

# ────────── Clientes (views/client.py) ──────────
from .views.client import (
    detalle_client, get_all_clients,
    create_client, update_client, delete_client,
    create_contact, update_contact,
)

# ────────── Usuarios (views/users.py) ──────────
from .views.users import (
    create_user, get_user, update_user, delete_user,
)

# ────────── Productos (views/products.py) ───────
from .views.products import (
    detalle_producto,
    get_all_products, create_product,
    update_productos, update_variant, delete_productos,
)



# ───────────────────────── URLPATTERNS ─────────────────────────
urlpatterns = [

    # ---------- Recuperación de contraseña ----------
# Mostrar formulario de recuperación y enviar correo
path('recuperar/', solicitar_reset, name='cliente_solicitar_reset'),

# Ruta del enlace del correo, muestra formulario de nueva contraseña si el token es válido
path('recuperar/<uidb64>/<token>/', reset_password_confirm, name='cliente_reset_password_confirm'),

# Ruta que recibe el POST con la nueva contraseña
path('recuperar/<uidb64>/<token>/submit/', reset_password_submit, name='cliente_reset_password_submit'),




path('recuperar/', solicitar_reset, name='cliente_solicitar_reset'),

    # ---------- Front-end ----------
    path('', index, name='index'),
    path('coleccion/<str:genero>/', genero_view, name='coleccion_genero'),
    path('registrarse/', registrarse, name='registrarse'),
    path('logout-client/', logout_client, name='logout_client'),

    path('create-client/', create_client, name='create_client'),
    path('login-client/',  login_client,  name='login_client'),

    # ---------- Dashboard ----------
    path('dashboard/login/',  login_user,  name='login_user'),
    path('dashboard/logout/', logout_user, name='logout_user'),
    path('dashboard/registro/', alta,            name='dashboard_alta'),
    path('dashboard/lista/',    lista_productos, name='dashboard_productos'),
    path('dashboard/productos/editar/<int:id>/',
         editar_producto, name='editar_producto'),

    # ---------- Productos ----------
    path('producto/<int:id>/',                      detalle_producto,  name='detalle_producto'),
    path('api/productos/',                          get_all_products,  name='get_all_products'),
    path('api/productos/crear/',                    create_product,    name='create_product'),
    path('api/productos/update/<int:id>/',          update_productos,  name='update_product'),
    path('api/productos/delete/<int:id>/',          delete_productos,  name='delete_product'),
    path('api/variantes/update/<int:variante_id>/',
         update_variant, name='update_variant'),
    path('api/categorias/',                         get_categorias,    name='get_categorias'),

    # ---------- Clientes ----------
    path('clientes/',                get_all_clients, name='get_all_clients'),
    path('clientes/<int:id>/',       detalle_client,  name='detalle_client'),
    path('clientes/crear/',          create_client,   name='create_client'),
    path('clientes/update/<int:id>/',update_client,   name='update_client'),
    path('clientes/delete/<int:id>/',delete_client,   name='delete_client'),
    path('contact/create/<int:id>/', create_contact,  name='create_contact'),
    path('contact/update/<int:id>/', update_contact,  name='update_contact'),

    # ---------- Usuarios ----------
    path('user/get/',          get_user,    name='get_user'),
    path('user/create/',       create_user, name='create_user'),
    path('user/update/<int:id>/', update_user, name='update_user'),
    path('user/delete/<int:id>/', delete_user, name='delete_user'),

    # ---------- Carrito ----------
    path('carrito/<int:id>/',                 detalle_carrito,  name='detalle_carrito'),
    path('carrito/crear/<int:cliente_id>/',   create_carrito,   name='create_carrito'),
    path('carrito/update/<int:id>/',          update_carrito,   name='update_carrito'),
    path('carrito/delete/<int:id>/',          delete_carrito,   name='delete_carrito'),

    # Alias para compatibilidad
    path('registro/', alta, name='alta'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
