from django.shortcuts import render
from misPerris.models import Mascota
from .serializers import MascotasSerializers
from rest_framework import generics

# Crear las vistas a presentar en el API

# presentara un listado de todas las mascotas ListAPIView (api que mostrara una lista)
class MascotasViewSet(generics.ListAPIView):
    queryset = Mascota.objects.all() # cuales seran los registros a presentar
    serializer_class = MascotasSerializers # cuales seran los campos a presentar

# presentar un listado y ademas la posibilidad de agregar registros ListCreateAPIView
class MascotasCrearViewSet(generics.ListCreateAPIView):
    queryset = Mascota.objects.all()
    serializer_class = MascotasSerializers

# presentar una pagina en donde podemos buscar una mascota
# por medio del ingreso de un parametro en su URL
# get_queryset()
class MascotasBuscarNombreViewSet(generics.ListAPIView):
    serializer_class = MascotasSerializers
    def get_queryset(self):
        nombre_mascota = self.kwargs['nombre'] # indicar el nombre del parametro
        return Mascota.objects.filter(nombre=nombre_mascota) # retornar las filas que cumplen con la condicion