from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, dama, caballero, detalles, get_all_products, create_product, get_categorias, alta

urlpatterns = [
    path('', index, name='index'),
    path('dama/', dama, name='dama'),
    path('caballero/', caballero, name='caballero'),
    path('detalles/', detalles, name='detalles'),
    path('api/productos/', get_all_products, name='get_all_products'),
    path('api/productos/crear/', create_product, name='create_product'),
    path('api/categorias/', get_categorias, name='get_categorias'),
    path('registro', alta, name='alta')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
