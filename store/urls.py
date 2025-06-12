from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, dama, caballero, detalle_producto, alta, editar_producto, get_all_products, create_product, get_categorias, update_productos, delete_productos, lista_productos

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
    path('api/categorias/', get_categorias, name='get_categorias')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
