# Integração de Sistemas  - Gestão de Frotas#
#Alunos Camoin Pamante e Sónia Pimentel#


from django.urls import path
from .import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_app, name='login'),
    path('logout_app/', views.logout_app, name='logout'),
    path('about/', views.about, name='about'),
    path('veiculoregister/', views.veiculoregister, name='veiculoregister'),
    path('listveiculos/', views.listveiculos, name='listveiculos'),
    path('registeruser/', views.registeruser, name='registeruser'),
    path('fazerpedido/<int:veiculo_id>/<int:id_user>/', views.fazerpedido, name='fazerpedido'),
    path('registarpedido/<int:veiculo_id>/', views.registarpedido, name='registarpedido'),
    path('veiculoList/', views.veiculoList, name='veiculoList'),
    path('pedidoList/', views.pedidoList, name='pedidoList'),
    path('notificationsadmin/<str:funcionario>/', views.notificationsadmin, name='notificationsadmin'),
    path('editarveiculo/<int:pk>/', views.editarveiculo, name='editarveiculo'),
    path('eliminarveiculo/<int:pk>/', views.eliminarveiculo, name='eliminarveiculo'),
    path('eliminarnotificacao/<int:pk>/', views.eliminarnotificacao, name='eliminarnotificacao'),
    path('veiculoeditado/<int:pk>/', views.veiculoeditado, name='veiculoeditado'),
    path('userList/', views.userList, name='userList'),
    path('editaruser/<int:pk>/', views.editaruser, name='editaruser'),
    path('editarpeido/<int:pk>/', views.editarpedido, name='editarpedido'),
    path('eliminaruser/<int:pk>/', views.eliminaruser, name='eliminaruser'),
    path('eliminarpedido/<int:pk>/', views.eliminarpedido, name='eliminarpedido'),
    path('usereditado/<int:pk>/', views.usereditado, name='usereditado'),
    path('find/', views.find, name='find'),
    path('findPedido/', views.findPedido, name='findPedido'),
    path('pesquisarVeiculo/', views.pesquisarVeiculo, name='pesquisarVeiculo'),
    path('confirmar/<int:pedido_id>/', views.confirmar, name='confirmar'),
    path('register/', views.register, name='register'),
    path('registeruseradmin/', views.registeruseradmin, name='registeruseradmin'),
    path('notificacao/<str:pk>', views.notificacao, name='notificacao'),
    path('pedidorejeitadoList/', views.pedidorejeitadoList, name='pedidorejeitadoList'),
   # path('novopedidoList/', views.novopedidoList, name='novopedidoList'),

]
