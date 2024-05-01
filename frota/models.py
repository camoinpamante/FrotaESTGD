# Integração de Sistemas  - Gestão de Frotas#
#Alunos Camoin Pamante e Sónia Pimentel#

import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def __str__(self):
        return f'{self.username},{self.is_staff}'


class Veiculo(models.Model):
    matricula = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    tipo_combustivel = models.CharField(max_length=50)
    description = models.TextField(max_length=100, blank=True, null=True, default='')
    image = models.ImageField(upload_to='uploads/veiculo')
    def __str__(self):
        return f'{self.marca}'

class Pedido(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userpedidos')
     veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='veiculopedido')
     data_inicio = models.DateField()
     data_fim = models.DateField()
     local = models.CharField(max_length=50)
     combustivel_inicial = models.IntegerField()
     combustivel_fim = models.IntegerField(default=0)
     kilometro_inicial = models.IntegerField(default=0)
     kilometro_final = models.IntegerField(default=0)
     confirmacao = models.BooleanField(default=False)

class Notification(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usernotification')
     funcionario = models.CharField(max_length=20)
     mensagem = models.CharField(max_length=100)
     confirmacao = models.BooleanField(default=False)


