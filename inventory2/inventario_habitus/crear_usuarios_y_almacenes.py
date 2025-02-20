import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_habitus.settings')
import django
django.setup()

from gestion_inventario.models import Usuario, Almacen
from django.contrib.auth.hashers import make_password

def crear_usuarios_y_almacenes():
    # Crear almacenes
    almacenes = [
        {'nombre': 'Alcala', 'responsable': 'Nicolas Gonzalez'},
        {'nombre': 'Faenza', 'responsable': 'Daniel Puin'},
        {'nombre': 'Habital', 'responsable': 'Camilo Agudelo'},
        {'nombre': 'Zetta55', 'responsable': 'Jhonatan Vargas'},
        {'nombre': 'Cabrera', 'responsable': 'Andrea Jaramillo'},
    ]
    for almacen_data in almacenes:
        Almacen.objects.get_or_create(**almacen_data)

    # Crear usuarios
    usuarios = [
        {
            'username': 'sistemas',
            'email': 'sistemas@habitusconstrucciones.com',
            'nombre': 'Jesus Saavedra',
            'perfil': 'superadmin',
            'password': 'zGaTL4sM@08',  # Contraseña alfanumérica de 8 dígitos
            'almacen': None,
        },
        {
            'username': 'Inventarios',
            'email': 'coordinacion@habitusconstrucciones.com',
            'nombre': 'Andrea Jaramillo',
            'perfil': 'superadmin',
            'password': '4ndrea1989',  # Contraseña alfanumérica de 8 dígitos
            'almacen': None,
        },
        {
            'username': 'Andrea',
            'email': 'postventahabitus@gmail.com',
            'nombre': 'Andrea Jaramillo',
            'perfil': 'admin',
            'password': 'andrea789',  # Contraseña alfanumérica de 8 dígitos
            'almacen': 'Cabrera',
        },
        {
            'username': 'Daniel',
            'email': 'dirfaenza@habitusconstrucciones.com',
            'nombre': 'Daniel Puin',
            'perfil': 'admin',
            'password': 'daniel01',  # Contraseña alfanumérica de 8 dígitos
            'almacen': 'Faenza',
        },
        {
            'username': 'Jhonatan',
            'email': 'dirzetta55@habitusconstrucciones.com',
            'nombre': 'Jhonatan Vargas',
            'perfil': 'admin',
            'password': 'jhonatan2',  # Contraseña alfanumérica de 8 dígitos
            'almacen': 'Zetta55',
        },
        {
            'username': 'Gustavo',
            'email': 'residentetecnicozetta55@habitusconstrucciones.com',
            'nombre': 'Gustavo Mora',
            'perfil': 'colaborador',
            'password': 'gustavo3',  # Contraseña alfanumérica de 8 dígitos
            'almacen': 'Zetta55',
        },
        {
            'username': 'Camilo',
            'email': 'dirhabital@habitusconstrucciones.com',
            'nombre': 'Camilo Agudelo',
            'perfil': 'admin',
            'password': 'camilo45',  # Contraseña alfanumérica de 8 dígitos
            'almacen': 'Habital',
        },
        {
            'username': 'Luisa',
            'email': 'planeacion@habitusconstrucciones.com',
            'nombre': 'Luisa Landinez',
            'perfil': 'colaborador',
            'password': 'luisa678',  # Contraseña alfanumérica de 8 dígitos
            'almacen': 'Habital',
        },
        {
            'username': 'Angie',
            'email': 'residentetecnicohabital@habitusconstrucciones.com',
            'nombre': 'Angie Rivera',
            'perfil': 'colaborador',
            'password': 'angie890',  # Contraseña alfanumérica de 8 dígitos
            'almacen': 'Habital',
        },
        {
            'username': 'Nicolas',
            'email': 'diralcala@habitusconstrucciones.com',
            'nombre': 'Nicolas Gonzalez',
            'perfil': 'admin',
            'password': 'nicolas9',  # Contraseña alfanumérica de 8 dígitos
            'almacen': 'Alcala',
        },
        {
            'username': 'Felipe',
            'email': 'residentetecnicoalcala@habitusconstrucciones.com',
            'nombre': 'Felipe Acosta',
            'perfil': 'colaborador',
            'password': 'felipe12',  # Contraseña alfanumérica de 8 dígitos
            'almacen': 'Alcala',
        },
    ]

    for usuario_data in usuarios:
        almacen_nombre = usuario_data.pop('almacen')
        if almacen_nombre:
            almacen = Almacen.objects.get(nombre=almacen_nombre)
        else:
            almacen = None

        # Verificar si el usuario ya existe
        usuario, creado = Usuario.objects.get_or_create(
            email=usuario_data['email'],
            defaults={
                'username': usuario_data['username'],
                'first_name': usuario_data['nombre'],
                'perfil': usuario_data['perfil'],
                'almacen': almacen,
                'password': make_password(usuario_data['password']),  # Encriptar la contraseña
            }
        )

        if not creado:
            # Si el usuario ya existe, actualizamos sus datos
            usuario.username = usuario_data['username']
            usuario.first_name = usuario_data['nombre']
            usuario.perfil = usuario_data['perfil']
            usuario.almacen = almacen
            usuario.password = make_password(usuario_data['password'])
            usuario.save()

        print(f"Usuario {'creado' if creado else 'actualizado'}: {usuario.username} - Contraseña: {usuario_data['password']}")

    print("Usuarios y almacenes creados/actualizados exitosamente.")

if __name__ == '__main__':
    crear_usuarios_y_almacenes()