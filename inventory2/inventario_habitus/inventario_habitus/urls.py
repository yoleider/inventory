"""
URL configuration for inventario_habitus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # Importa 'include' para incluir las URLs de la aplicación
from gestion_inventario.views import send_test_email, inicio, buscar_item, solicitar_traslado  # Importa las vistas
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('send-test-email/', send_test_email, name='send_test_email'),  # Ruta para enviar correos de prueba
    path('inventario/', include('gestion_inventario.urls')),  # Incluye las URLs de la aplicación gestion_inventario
    path('accounts/', include('django.contrib.auth.urls')),  # URLs de autenticación
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]