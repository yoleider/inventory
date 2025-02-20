from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelo para los usuarios personalizados
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)  # Campo de correo electrónico
    perfil = models.CharField(max_length=20, choices=[
        ('superadmin', 'Super-administrador'),
        ('admin', 'Administrador de almacén'),
        ('colaborador', 'Colaborador'),
    ])  # Campo para definir el perfil del usuario
    almacen = models.ForeignKey('Almacen', on_delete=models.SET_NULL, null=True, blank=True)  # Relación con el almacén

    def __str__(self):
        return self.username  # Representación en texto del usuario

# Modelo para los almacenes
class Almacen(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del almacén
    responsable = models.CharField(max_length=100)  # Nombre del responsable

    def __str__(self):
        return self.nombre  # Representación en texto del almacén

# Modelo para los ítems del inventario
class Item(models.Model):
    codigo = models.CharField(max_length=50, unique=True)  # Código único del ítem
    descripcion = models.CharField(max_length=200)  # Descripción del ítem
    categoria = models.CharField(max_length=50)  # Categoría (material, herramienta, etc.)
    uso = models.BooleanField(default=True)  # ¿Está en uso?
    unidad = models.CharField(max_length=10)  # Unidad de medida (ML, UND, etc.)
    cantidad_inicial = models.IntegerField()  # Cantidad inicial
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Valor unitario
    cantidad_actual = models.IntegerField()  # Cantidad actual
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)  # Valor total
    observacion = models.TextField(blank=True)  # Observaciones (opcional)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)  # Relación con el almacén

    def __str__(self):
        return self.descripcion  # Representación en texto del ítem

# Modelo para las solicitudes de traslado
class SolicitudTraslado(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # Relación con el ítem
    almacen_origen = models.ForeignKey(Almacen, related_name='traslados_origen', on_delete=models.CASCADE)  # Almacén de origen
    almacen_destino = models.ForeignKey(Almacen, related_name='traslados_destino', on_delete=models.CASCADE)  # Almacén de destino
    cantidad = models.IntegerField()  # Cantidad a trasladar
    solicitante = models.ForeignKey(Usuario, related_name='solicitudes', on_delete=models.CASCADE)  # Usuario que solicita
    aprobado_por_admin_almacen = models.BooleanField(default=False)  # Aprobación del administrador del almacén
    aprobado_por_superadmin = models.BooleanField(default=False)  # Aprobación del super-administrador
    fecha_solicitud = models.DateTimeField(auto_now_add=True)  # Fecha de la solicitud

    def __str__(self):
        return f"Traslado de {self.item} a {self.almacen_destino}"  # Representación en texto de la solicitud