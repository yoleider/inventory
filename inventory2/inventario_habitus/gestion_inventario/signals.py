from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import SolicitudTraslado

@receiver(post_save, sender=SolicitudTraslado)
def notificar_solicitud_traslado(sender, instance, created, **kwargs):
    if created:
        subject = f"Nueva solicitud de traslado: {instance.item}"
        message = (
            f"Se ha creado una nueva solicitud de traslado:\n\n"
            f"Item: {instance.item}\n"
            f"Almacén de origen: {instance.almacen_origen}\n"
            f"Almacén de destino: {instance.almacen_destino}\n"
            f"Cantidad: {instance.cantidad}\n"
            f"Solicitante: {instance.solicitante}\n"
        )
        send_mail(
            subject,
            message,
            'inventario@habitusconstrucciones.com',
            ['sistemas@habitusconstrucciones.com', 'coordinacion@habitusconstrucciones.com'],
            fail_silently=False,
        )