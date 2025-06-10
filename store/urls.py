from django.urls import path
from .views import index, dama, caballero, detalles

urlpatterns = [
    path('', index, name='index'),
    path('dama/', dama, name='dama'),
    path('caballero/', caballero, name='caballero'),
    path('detalles/', detalles, name='detalles'),
]
