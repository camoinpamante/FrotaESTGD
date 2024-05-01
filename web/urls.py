# Integração de Sistemas  - Gestão de Frotas#
#Alunos Camoin Pamante e Sónia Pimentel#

from django.urls import path

from .import views

urlpatterns = [

    path('', views.index, name='index'),
]


