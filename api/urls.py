from django.conf.urls import url
from rest_framework import urlpatterns
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

# definir las direcciones ULS que seran ocupadas por las APIS
# url(r'^ --ruta de la api-- $',nombre del view a ver)
# (?P<nombre parametro>) 
# .+ -> de una a mas caracteres 
# [0-9]+  -> de uno a mas digitos
urlPatterns = [
    url(r'^api/mascotas/$',views.MascotasViewSet.as_view()),
    url(r'^api/mascotas_agregar/$',views.MascotasCrearViewSet.as_view()),
    url(r'^api/mascota_buscar/(?P<nombre>.+)/$',views.MascotasBuscarNombreViewSet.as_view())
]

# el format_suffix_patterns permite reconocer el patron de ruta 
# como una direccion valida del rest_framework 
urlpatterns=format_suffix_patterns(urlPatterns)