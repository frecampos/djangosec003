from django.db.models import fields
from misPerris.models import Mascota
from rest_framework import serializers

# indicar la clase que contendra el modelo a serializar
# y la lista de sus campos
class MascotasSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mascota #modelo a serializar
        #fields = ["nombre","edad","descripcion","imagen","categoria"] # lista de los campos
        fields = "__all__"