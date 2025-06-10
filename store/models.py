from django.db import models

class Cliente(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class Usuario(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    genero = models.CharField(max_length=50)
    en_oferta = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Carrito(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="vacio")
    created_at = models.DateTimeField(auto_now_add=True)

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

class Wishlist(models.Model):
    user = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)

class Orden(models.Model):
    carrito = models.OneToOneField(Carrito, on_delete=models.CASCADE)
    user = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class OrdenDetalle(models.Model):
    order = models.ForeignKey(Orden, on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

class ContactoCliente(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, primary_key=True)
    nombre = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    mensaje = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
