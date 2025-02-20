import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import SolicitudTraslado

class NotificacionesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                f'notificaciones_{self.user.id}',
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                f'notificaciones_{self.user.id}',
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def notificar_traslado(self, event):
        solicitud_id = event['solicitud_id']
        solicitud = await sync_to_async(SolicitudTraslado.objects.get)(id=solicitud_id)
        await self.send(text_data=json.dumps({
            'type': 'notificacion',
            'message': f'Nueva solicitud de traslado: {solicitud.item.descripcion}',
        }))

    async def notificar_aprobacion(self, event):
        solicitud_id = event['solicitud_id']
        solicitud = await sync_to_async(SolicitudTraslado.objects.get)(id=solicitud_id)
        await self.send(text_data=json.dumps({
            'type': 'notificacion',
            'message': f'Solicitud de traslado aprobada: {solicitud.item.descripcion}',
        }))