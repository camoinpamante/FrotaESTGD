
from django.urls import path
from .import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_app, name='login'),
    path('logout_app/', views.logout_app, name='logout'),
    path('departamento/', views.registerDepartamento, name='departamento'),
    path('about/', views.about, name='about'),
    path('veiculoregister/', views.veiculoregister, name='veiculoregister'),
    path('listveiculos/', views.listveiculos, name='listveiculos'),
    path('registeruser/', views.registeruser, name='registeruser'),
    path('fazerpedido/<int:id>/', views.fazerpedido, name='fazerpedido')
]
