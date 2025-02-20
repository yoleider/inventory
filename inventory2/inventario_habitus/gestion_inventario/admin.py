from django.contrib import admin
from .models import Usuario, Almacen, Item, SolicitudTraslado

admin.site.register(Usuario)
admin.site.register(Almacen)
admin.site.register(Item)
admin.site.register(SolicitudTraslado)