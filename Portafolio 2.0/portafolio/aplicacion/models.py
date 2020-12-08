from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from .managers import UserManager, AgregarReservaManager, VentaManager, ReservaDetalleManager
from django.conf import settings
from datetime import datetime, date
import datetime
from django.db.models.signals import post_save
import random
from model_utils.models import TimeStampedModel

def random_string():
    return str(random.randint(10000, 99999))

class User(AbstractBaseUser, PermissionsMixin):
    cli_Rut=models.CharField('Rut',max_length=30, unique=True)
    cli_Nombre=models.CharField('Nombre',max_length=30, blank=True)
    cli_Apellidos=models.CharField('Apellidos',max_length=30, blank=True)
    cli_Edad= models.IntegerField('Edad', blank=True, null=True, default="0")
    cli_Nacionalidad=models.CharField('Nacionalidad',max_length=30, blank=True)
    email= models.EmailField('Correo', blank=True)
    cli_Telefono=models.CharField('Telefono',max_length=15, blank=True)
    username = models.CharField(max_length=10, unique=True)
    codregistro = models.CharField(max_length=6, blank=True, default='000000')
    funcionario = models.BooleanField(default=False)
    #
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False) 

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['cli_Rut', 'cli_Nombre','cli_Apellidos','cli_Edad','cli_Nacionalidad','email','cli_Telefono']

    objects = UserManager()

    def get_full_name (self):
        return self.cli_Nombre + ' ' + self.cli_Apellidos

class Acompañante(models.Model):
    acom_rut=models.CharField('Rut',max_length=14, unique=True)
    acom_nombre=models.CharField('Nombre',max_length=30)
    acom_apellidos=models.CharField('Apellidos',max_length=30)
    acom_edad= models.IntegerField('Edad',null=True, default="0")
    acom_nacionalidad=models.CharField('Nacionalidad',max_length=30)
    acom_email= models.EmailField('Correo', unique=True)
    acom_telefono=models.CharField('Telefono',max_length=12)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__ (self):
        return self.acom_rut

#def quitar_relacion_user_acompañante(sender, instance, **kwargs):
#    usuario = instance.id
#    acompañantes = Acompañante.objects.filter(user_id=usuario)
#    for acompañantt in acompañantes:
#        acompañantt.user_id.remove(usuario)

#post_save.connect(quitar_relacion_user_acompañante, sender = User)

class Inventario(models.Model):
    reparacion= models.CharField(max_length=100, default="")
    mejoramiento= models.CharField(max_length=100, default="")

    def __str__ (self):
        return self.reparacion

class Ciudad(models.Model):
    descrip_ciudad=models.CharField(max_length=100, default="")

    def __str__ (self):
        return self.descrip_ciudad

class Comuna(models.Model):
    descrip_comuna=models.CharField(max_length=100, default="")
    ciudad=models.ForeignKey(Ciudad, on_delete=models.CASCADE)

    def __str__ (self):
        return self.descrip_comuna

class Departamento(TimeStampedModel):

    CALE_CHOICES = (
        ('Si', 'Si'),
        ('No', 'No'),
    )
    INTERNET_CHOICES = (
        ('Si', 'Si'),
        ('No', 'No'),
    )
    AMOBLADO_CHOICES = (
        ('Si', 'Si'),
        ('No', 'No'),
    )
    TELEVICION_CHOICES = (
        ('Si', 'Si'),
        ('No', 'No'),
    )
    DISPONIBILIDADDEPART_CHOICES = (
        ('Si', 'Si'),
        ('No', 'No'),
    )
    Codigo = models.CharField(max_length=3, unique=True, default="")
    Nombre_Departamento = models.CharField(max_length=30)
    Numero_propiedad = models.IntegerField(null=True, default="0")
    Descripcion_departamento= models.CharField(max_length=200, default="")
    Direccion_departamento= models.CharField(max_length=200, default="")
    habitaciones = models.IntegerField(null=True, default="0")
    Baños = models.IntegerField(null=True, default="0")    
    Calefaccion = models.CharField(max_length=2, choices=CALE_CHOICES, default="Si")
    Internet = models.CharField(max_length=2, choices=INTERNET_CHOICES, default="Si")
    Amoblado = models.CharField(max_length=2, choices=AMOBLADO_CHOICES, default="Si")
    Televicion = models.CharField(max_length=2, choices=TELEVICION_CHOICES, default="Si")
    Imagen_Recinto = models.ImageField( upload_to="departamento/", null=True, blank=True, default="/static/img/logo.PNG")
    Imagen_Entorno = models.ImageField( upload_to="", null=True, blank=True)
    Valor_Diario = models.FloatField(default="0")
    Disponible = models.CharField(max_length=2, choices=DISPONIBILIDADDEPART_CHOICES, default="Si")
    comuna=models.ForeignKey(Comuna, on_delete=models.CASCADE, default="")
    inventario = models.OneToOneField(Inventario, unique=True, on_delete=models.CASCADE, default="")
    dividendo = models.IntegerField(default="0")
    contribucion = models.IntegerField(default="0")
    numero_venta = models.PositiveIntegerField('numero de ventas',default=0)
    precio_compra =models.DecimalField('precio compra',max_digits=7, decimal_places=2, default=0)

    def __str__ (self):
        return self.Nombre_Departamento

class Vehiculo(models.Model):
    AIRE_CHOICES = (
        ('Si', 'Si'),
        ('No', 'No'),
    )
    DISPONIBILIDADVEHICULO_CHOICES = (
        ('Si', 'Si'),
        ('No', 'No'),
    )
    patente=models.CharField('Patente',max_length=14, unique=True)
    color_vehiculo=models.CharField('Color Vehiculo',max_length=30)
    cant_puerta=models.IntegerField('Puertas',null=True, default="0")
    aire_acondicionado=models.CharField('Color Vehiculo',max_length=30, choices=AIRE_CHOICES, default="Si")
    cant_asiento=models.IntegerField('Asiento',null=True, default="0")
    disponibilidad_vehi=models.CharField('Color Vehiculo',max_length=30, choices=DISPONIBILIDADVEHICULO_CHOICES, default="Si")
    imagen_vehiculo = models.ImageField( default="", blank=True, null=True)
    modelo=models.CharField(max_length=30, default="")
    marca=models.CharField(max_length=30, default="")

    def __str__ (self):
        return self.patente  

class Conductor(models.Model):
    cond_rut=models.CharField('Rut',max_length=14, unique=True)
    cond_nombre=models.CharField('Nombre',max_length=30)
    cond_apellidos=models.CharField('Apellidos',max_length=30)
    cond_edad= models.IntegerField('Edad', default="0")
    cond_nacionalidad=models.CharField('Nacionalidad',max_length=30)
    cond_email= models.EmailField('Correo',blank=True)
    cond_telefono=models.CharField('Telefono',max_length=12)
    vehiculo=models.ManyToManyField(Vehiculo)

    def __str__ (self):
        return self.cond_nombre

class Tour(models.Model):
    
    CATEGORIATOUR_CHOICES = (
        ('Tour City', 'Tour City'),
        ('Turismo Aventura', 'Turismo Aventura'),
    )
    COMESTIBLE_CHOICES = (
        ('Si', 'Si'),
        ('No', 'No'),
    )
    descripcion_tour=models.CharField(max_length=100, default="")
    categoria=models.CharField(max_length=100, choices=CATEGORIATOUR_CHOICES, default="Tour City")
    comestible=models.CharField(max_length=100, choices=COMESTIBLE_CHOICES, default="Si")
    valor_tour=models.IntegerField('Valor', default='0')
    imagen_tour = models.ImageField( default="", blank=True, null=True)

    def __str__ (self):
        return self.categoria


class ServicioExtra(models.Model):
    descrip_servicio=models.CharField('Descripcion Servicios',max_length=20)
    direccion_reunion=models.CharField('Reunion',max_length=50)
    direccion_destino=models.CharField('Desatino',max_length=50)
    fecha_encuentro=models.DateField('Fecha encuentro', default=datetime.date.today)
    fecha_termino_servicio=models.DateField('Fecha Termino', default=datetime.date.today)
    valor_servicio=models.IntegerField('Valor', default="0")
    conductor=models.ForeignKey(Conductor, on_delete=models.CASCADE, null=True, blank=True)
    tour=models.ForeignKey(Tour, on_delete=models.CASCADE, null=True, blank=True)

    def __str__ (self):
        return self.descrip_servicio     

class Reserva(models.Model):

    CHECK_CHOICES = (
        ('NoCheck', 'NoCheck'),
        ('CheckIn', 'CheckIn'),
        ('CheckOut', 'CheckOut'),
    )
    Codigo_Reserva = models.CharField(max_length=5, default = random_string, unique=True)
    Fecha_Reserva_Inicio = models.DateField(blank=True, default=datetime.date.today)   
    Fecha_Reserva_Termino = models.DateField(blank=True, default=datetime.date.today)
    Cantidad_Dias=models.IntegerField('Valor', default="0")
    Estado_Reserva = models.BooleanField(default=False)
    check=models.CharField(max_length=100, default="No Check", choices=CHECK_CHOICES)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default="")
    departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE, default="")
    servicioextra=models.ManyToManyField(ServicioExtra, null=True, blank=True)

    def __str__ (self):
        return self.Codigo_Reserva

class Contact(models.Model):
    asunto = models.CharField(max_length=50)
    descripcioncontacto = models.TextField()
    correoaenviar = models.EmailField(default="")

    def __str__(self):
        return self.asunto

class Venta(TimeStampedModel):

    # tipo recibo constantes
    BOLETA = '0'
    FACTURA = '1'
    SIN_COMPROBANTE = '2'
    # tipo pago constantes
    TARJETA = '0'
    CASH = '1'
    BONO = '2'
    OTRO = '3'
    #
    TIPO_INVOCE_CHOICES = [
        (BOLETA, 'Boleta'),
        (FACTURA, 'Factura'),
        (SIN_COMPROBANTE, 'Sin Comprobante'),
    ]

    TIPO_PAYMENT_CHOICES = [
        (TARJETA, 'Tarjeta'),
        (CASH, 'Cash'),
        (BONO, 'Bono'),
        (OTRO, 'Otro'),
    ]

    date_sale = models.DateTimeField(
        'Fecha de Venta',
    )
    count = models.PositiveIntegerField('Cantidad de Productos')
    amount = models.DecimalField(
        'Monto', 
        max_digits=10, 
        decimal_places=2
    )
    type_invoce = models.CharField(
        'TIPO',
        max_length=2,
        choices=TIPO_INVOCE_CHOICES
    )
    type_payment = models.CharField(
        'TIPO PAGO',
        max_length=2,
        choices=TIPO_PAYMENT_CHOICES
    )
    close = models.BooleanField(
        'Venta cerrada',
        default=False
    )
    anulate = models.BooleanField(
        'Venta Anulada',
        default=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='cajero',
        related_name="user_venta",
    )

    objects = VentaManager()

class Reservando(TimeStampedModel):
    Codigo = models.CharField(max_length=3, unique=True)
    count = models.PositiveIntegerField('Cantidad')
    departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE, default="")
    Estado_Reservas = models.BooleanField(default=False)
    Codigo_Reservas = models.CharField(max_length=5, default = random_string, unique=True)
    total_cobrar = models.FloatField(default="0")
    Fecha_Reserva_Inicios = models.DateField(blank=True, default=datetime.date.today)   
    Fecha_Reserva_Terminos = models.DateField(blank=True, default=datetime.date.today)
    servicioextra=models.ManyToManyField(ServicioExtra, null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default="")

    objects = AgregarReservaManager()
    
    def __str__ (self):
        return self.Codigo_Reservas

class Multa(models.Model):
    descrip_multa=models.CharField(max_length=100, default="")
    monto_multa=models.IntegerField('Valor', default="0")
    estado_multa=models.BooleanField(default=False)
    reserva=models.ForeignKey(Reservando, on_delete=models.CASCADE, null=True, blank=True)

class ReservaDetalle(TimeStampedModel):

    departamento = models.ForeignKey(Departamento,on_delete=models.CASCADE, related_name='departamento_venta')
    venta = models.ForeignKey(Venta,on_delete=models.CASCADE, related_name='detail_sale')
    count = models.PositiveIntegerField('Cantidad')
    price_purchase = models.DecimalField('Precio Compra', max_digits=10, decimal_places=3)
    price_sale = models.DecimalField('Precio Venta', max_digits=10, decimal_places=2)
    tax = models.DecimalField('Impuesto', max_digits=5,decimal_places=2)
    anulate = models.BooleanField(default=False)

    objects = ReservaDetalleManager()