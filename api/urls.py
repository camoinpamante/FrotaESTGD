# Integração de Sistemas  - Gestão de Frotas#
#Alunos Camoin Pamante e Sónia Pimentel#

# Urls com as respectivas views para os caminhos#
from django.urls import path
from .import views
urlpatterns = [
 path('pedidos/', views.ListESTGDAPIView.as_view()),
 path('pedidos/<int:pk>/', views.crudESTGDAPIView.as_view()),
 path('veiculos/', views.ListVeiculoESTGDAPIView.as_view()),
 path('veiculos/<int:pk>/', views.crudVeiculoESTGDAPIView.as_view()),
 path('utilizador/', views.ListUtilizadorESTGDAPIView.as_view()),
 path('utilizador/<int:pk>/', views.crudUtilizadorESTGDAPIView.as_view()),
 path('login/', views.LoginView.as_view())
]