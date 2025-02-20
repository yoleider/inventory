from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from openpyxl import Workbook
from django.http import HttpResponse
from django.contrib import messages  # Importamos messages para mostrar notificaciones
from .models import Item, Almacen, SolicitudTraslado
from .forms import SolicitudTrasladoForm
import csv  # Importamos csv para generar informes
from django.core.paginator import Paginator
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@login_required
def inicio(request):
    items_list = Item.objects.all()
    paginator = Paginator(items_list, 10)  # Muestra 10 ítems por página
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)
    return render(request, 'gestion_inventario/inicio.html', {'items': items})

@login_required
def buscar_item(request):
    """
    Vista para buscar ítems por descripción.
    """
    query = request.GET.get('q')
    if query:
        items = Item.objects.filter(descripcion__icontains=query)
    else:
        items = Item.objects.all()
    return render(request, 'gestion_inventario/buscar_item.html', {'items': items})

@login_required
def solicitar_traslado(request, item_id):
    """
    Vista para solicitar un traslado de un ítem.
    """
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = SolicitudTrasladoForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.item = item
            solicitud.solicitante = request.user
            solicitud.almacen_origen = item.almacen  # Asignar el almacén de origen
            solicitud.save()

            # Enviar correo de notificación
            subject = f"Nueva solicitud de traslado: {item.descripcion}"
            message = (
                f"Se ha creado una nueva solicitud de traslado:\n\n"
                f"Item: {item.descripcion}\n"
                f"Almacén de origen: {item.almacen}\n"
                f"Almacén de destino: {solicitud.almacen_destino}\n"
                f"Cantidad: {solicitud.cantidad}\n"
                f"Solicitante: {request.user.username}\n"
            )
            send_mail(
                subject,
                message,
                'inventario@habitusconstrucciones.com',
                ['sistemas@habitusconstrucciones.com', 'coordinacion@habitusconstrucciones.com'],
                fail_silently=False,
            )

            return redirect('inicio')
    else:
        form = SolicitudTrasladoForm()
    return render(request, 'gestion_inventario/solicitar_traslado.html', {'form': form, 'item': item})

def send_test_email(request):
    """
    Vista de prueba para enviar un correo electrónico.
    """
    send_mail(
        'Asunto del correo de prueba',
        'Este es el cuerpo del correo de prueba.',
        'inventario@habitusconstrucciones.com',  # Remitente
        ['sistemas@habitusconstrucciones.com'],  # Lista de destinatarios
        fail_silently=False,
    )
    return HttpResponse("Correo enviado correctamente.")

# ==================================================
# Nuevo código agregado para la aprobación de traslados
# ==================================================

@login_required
def aprobar_traslado(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudTraslado, id=solicitud_id)
    
    if request.user.perfil == 'admin' and request.user.almacen == solicitud.almacen_origen:
        solicitud.aprobado_por_admin_almacen = True
        solicitud.save()
        messages.success(request, 'Solicitud aprobada por el administrador del almacén.')
    elif request.user.perfil == 'superadmin':
        solicitud.aprobado_por_superadmin = True
        solicitud.save()
        messages.success(request, 'Solicitud aprobada por el super-administrador.')
    else:
        messages.error(request, 'No tienes permiso para aprobar esta solicitud.')

    # Enviar notificación
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notificaciones_{solicitud.solicitante.id}',
        {
            'type': 'notificar_traslado',
            'solicitud_id': solicitud.id,
        }
    )

    return redirect('lista_solicitudes')

@login_required
def lista_solicitudes(request):
    if request.user.perfil == 'superadmin':
        solicitudes_list = SolicitudTraslado.objects.all()
    elif request.user.perfil == 'admin':
        solicitudes_list = SolicitudTraslado.objects.filter(almacen_origen=request.user.almacen)
    else:
        solicitudes_list = SolicitudTraslado.objects.filter(solicitante=request.user)
    
    paginator = Paginator(solicitudes_list, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    solicitudes = paginator.get_page(page_number)
    
    return render(request, 'gestion_inventario/lista_solicitudes.html', {'solicitudes': solicitudes})

# ==================================================
# Nuevo código agregado para la generación de informes
# ==================================================

@login_required
def generar_informe(request, tipo):
    if request.user.perfil != 'superadmin':
        return HttpResponse('No tienes permiso para generar informes.', status=403)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="informe_{tipo}.xlsx"'

    wb = Workbook()
    ws = wb.active

    if tipo == 'almacen':
        ws.append(['Almacén', 'Responsable', 'Total de ítems', 'Valor total'])
        for almacen in Almacen.objects.all():
            items = Item.objects.filter(almacen=almacen)
            total_items = items.count()
            valor_total = sum(item.valor_total for item in items)
            ws.append([almacen.nombre, almacen.responsable, total_items, valor_total])
    elif tipo == 'movimientos':
        ws.append(['Item', 'Almacén origen', 'Almacén destino', 'Cantidad', 'Solicitante', 'Fecha'])
        for solicitud in SolicitudTraslado.objects.all():
            ws.append([
                solicitud.item.descripcion,
                solicitud.almacen_origen.nombre,
                solicitud.almacen_destino.nombre,
                solicitud.cantidad,
                solicitud.solicitante.username,
                solicitud.fecha_solicitud.strftime('%Y-%m-%d %H:%M:%S'),
            ])
    elif tipo == 'total':
        ws.append(['Item', 'Descripción', 'Cantidad actual', 'Valor total', 'Almacén'])
        for item in Item.objects.all():
            ws.append([item.codigo, item.descripcion, item.cantidad_actual, item.valor_total, item.almacen.nombre])

    wb.save(response)
    return response