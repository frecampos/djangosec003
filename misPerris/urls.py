from django.contrib import admin
from django.urls import path, include
from .views import buscar_nombre, insertar_galeria, devolver, admin_usuario, adoptar, modificar, buscar_modificar, eliminar,crear_usuario,cerrar_sesion,inicio, galeria, formulario, registro, ficha_mascota, filtrar_categoria,filtrar_descripcion, filtrar_cate, login

urlpatterns = [
    path('',inicio,name='IND'),
    path('galeria/',galeria,name='GALE'),
    path('formulario/', formulario,name='FORMU'),
    path('registro/',registro,name='REG'),
    path('ficha_mascota/<id>/',ficha_mascota,name='FICHAM'),
    path('filtrar_c/',filtrar_categoria,name='FILTRARC'),
    path('filtrar_d/',filtrar_descripcion, name='FILTRARD'),
    path('filtrar_cate/<id>/',filtrar_cate,name='FILTRARCATE'),
    path('login/',login, name='LOGIN'),
    path('cerrar/',cerrar_sesion,name='CERRAR'),
    path('crear_usuario/',crear_usuario,name='CREARU'),
    path('eliminar/<id>/',eliminar,name='ELIMINAR'),
    path('modificar/<id>/',buscar_modificar,name='BUSCARMODI'),
    path('modifica/',modificar,name='MODI'),
    path('adoptar/<id>/',adoptar,name='ADOPTAR'),
    path('admin_usuario/',admin_usuario,name='ADMINUSUARIO'),
    path('devolver/<id>/',devolver,name='DEVOLVER'),
    path('insertar_galeria/',insertar_galeria,name='INSERTARG'),
    path('buscar_nombre/',buscar_nombre,name='BUSCARM'),
]

# {% url '' %}