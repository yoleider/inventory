from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Ruta para la página de inicio
    path('buscar/', views.buscar_item, name='buscar_item'),  # Ruta para buscar ítems
    path('solicitar/<int:item_id>/', views.solicitar_traslado, name='solicitar_traslado'),  # Ruta para solicitar traslados
    path('solicitudes/', views.lista_solicitudes, name='lista_solicitudes'),
    path('aprobar/<int:solicitud_id>/', views.aprobar_traslado, name='aprobar_traslado'),
    path('informe/<str:tipo>/', views.generar_informe, name='generar_informe'),
]