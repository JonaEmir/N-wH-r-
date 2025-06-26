from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# ——————————————————————————————————————
# Modelos de usuario y cliente
# ——————————————————————————————————————



class ClienteManager(BaseUserManager):
    def create_user(self, username, correo, nombre, password=None, telefono=None, direccion=None):
        """
        Crea y guarda un Cliente con username, correo y nombre obligatorios,
        y teléfono y dirección opcionales.
        """
        if not username:
            raise ValueError("El usuario debe tener un username")
        if not correo:
            raise ValueError("El usuario debe tener un correo electrónico")
        if not nombre:
            raise ValueError("El usuario debe tener un nombre")

        cliente = self.model(
            username=username,
            correo=correo,
            nombre=nombre,
            telefono=telefono,
            direccion=direccion
        )
        cliente.set_password(password)
        cliente.save(using=self._db)
        return cliente

    def create_superuser(self, username, correo, nombre, password):
        cliente = self.create_user(
            username=username,
            correo=correo,
            nombre=nombre,
            password=password
        )
        cliente.is_admin = True
        cliente.save(using=self._db)
        return cliente

class Cliente(AbstractBaseUser):
    username   = models.CharField(max_length=255, unique=True)
    correo     = models.EmailField(max_length=255, blank=True)
    nombre     = models.CharField(max_length=255, null=True)
    telefono   = models.CharField(max_length=20, blank=True, null=True)
    direccion  = models.CharField(max_length=500, blank=True, null=True)

    is_active  = models.BooleanField(default=True)
    is_admin   = models.BooleanField(default=False)

    objects    = ClienteManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['correo', 'nombre']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Usuario(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role     = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username} ({self.role})"


# ——————————————————————————————————————
# Categorías y Productos
# ——————————————————————————————————————

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre      = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio      = models.DecimalField(max_digits=10, decimal_places=2)
    categoria   = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    genero      = models.CharField(max_length=50)
    en_oferta   = models.BooleanField(default=False)
    imagen      = models.ImageField(upload_to='productos/', blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    @property
    def stock_total(self):
        """
        Suma el stock de todas sus variantes.
        Útil para mostrar stock global de un producto con variantes.
        """
        return sum( var.stock for var in self.variantes.all() )


# ——————————————————————————————————————
# Sistema de variantes (tallas, colores, etc.)
# ——————————————————————————————————————

class Atributo(models.Model):
    """
    Define un tipo de atributo de variante (ej. 'Talla', 'Color').
    """
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class AtributoValor(models.Model):
    """
    Valores específicos de un atributo (ej. talla '38', color 'Rojo').
    """
    atributo = models.ForeignKey(Atributo, on_delete=models.CASCADE, related_name="valores")
    valor     = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.atributo.nombre}: {self.valor}"

class Variante(models.Model):
    """
    Cada Variante es una versión de Producto con atributos (talla, color…)
    y su propio stock/precio/SKU si fuera necesario.
    """
    producto   = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="variantes")
    sku        = models.CharField(max_length=100, blank=True, null=True,
                                  help_text="Código interno o UPC opcional")
    precio     = models.DecimalField(max_digits=10, decimal_places=2,
                                     blank=True, null=True,
                                     help_text="Si varía de precio respecto al Producto")
    stock      = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        attrs = ", ".join(str(av) for av in self.attrs.all())
        return f"{self.producto.nombre} ({attrs})" if attrs else self.producto.nombre

class VarianteAtributo(models.Model):
    """
    Relaciona cada Variante con sus valores de atributo.
    """
    variante       = models.ForeignKey(Variante, on_delete=models.CASCADE, related_name="attrs")
    atributo_valor = models.ForeignKey(AtributoValor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("variante", "atributo_valor")

    def __str__(self):
        return f"{self.variante} → {self.atributo_valor}"


# ——————————————————————————————————————
# Carrito, Wishlist y Órdenes
# ——————————————————————————————————————

class Carrito(models.Model):
    cliente    = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    status     = models.CharField(max_length=50, default="vacio")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.cliente.username} ({self.status})"

class CarritoProducto(models.Model):
    carrito  = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    variante = models.ForeignKey(Variante, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.variante} en {self.carrito}"

class Wishlist(models.Model):
    cliente   = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, blank=True, related_name='wishlists')

    def __str__(self):
        # Listamos los nombres de todos los productos en la wishlist
        nombres = ", ".join(p.nombre for p in self.productos.all())
        return f"{self.cliente.username} quiere {nombres}"

class Orden(models.Model):
    carrito        = models.OneToOneField(Carrito, on_delete=models.CASCADE)
    cliente        = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total_amount   = models.DecimalField(max_digits=10, decimal_places=2)
    status         = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.cliente.username}"

class OrdenDetalle(models.Model):
    order          = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name="detalles")
    variante       = models.ForeignKey(Variante, on_delete=models.CASCADE)
    cantidad       = models.IntegerField()
    precio_unitario= models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}×{self.variante} en Orden #{self.order.id}"


# ——————————————————————————————————————
# Contacto de clientes
# ——————————————————————————————————————

class ContactoCliente(models.Model):
    cliente    = models.OneToOneField(Cliente, on_delete=models.CASCADE, primary_key=True)
    nombre     = models.CharField(max_length=255)
    email      = models.CharField(max_length=255)
    mensaje    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contacto de {self.cliente.username}"
