# Integração de Sistemas  - Gestão de Frotas#
#Alunos Camoin Pamante e Sónia Pimentel#

#Bibliotecas
from rest_framework import serializers
from frota.models import Veiculo, User, Pedido

# Criação das classes  Serializers Veículo;Utilizador;Pedido e login#
class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()