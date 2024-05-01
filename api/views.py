# Integração de Sistemas  - Gestão de Frotas#
#Alunos Camoin Pamante e Sónia Pimentel#

#Ficheiro contém as class e respectivas funções para listar pedidos (GET/POST/PUT/Delete)
#Ficheiro contém as class e respectivas funções para listar veículo (GET/POST/PUT/Delete)
#Ficheiro contém as class e respectivas funções para listar utilizador (GET/POST/PUT/Delete)
# Login de utilizador
from contextvars import Token

from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import  APIView
from .serializers import VeiculoSerializer, PedidoSerializer, UserSerializer, LoginSerializer
from frota.models import Veiculo, Pedido, User


# criação das views.#
class ListESTGDAPIView(APIView):
    def get(self, request):
        pedido = Pedido.objects.filter(user=request.user.id)
        serializer = PedidoSerializer(pedido, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#Class CRUD pedido
class crudESTGDAPIView(APIView):
    def delete(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk, user=request.user)
        pedido.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        serializer = PedidoSerializer(pedido,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class Veiculo (GET/PUT/Delete)

class VeiculoAPIView(APIView):
    def get(self, request, pk):
        veiculo = get_object_or_404(Veiculo, pk=pk, user=request.user)
        serializer = VeiculoSerializer(veiculo, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        veiculo = get_object_or_404(Veiculo, pk=pk)
        serializer = VeiculoSerializer(veiculo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        veiculo = get_object_or_404(Veiculo, id=pk, user=request.user)
        veiculo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#lista de veículos (GET/POST)
class ListVeiculoESTGDAPIView(APIView):
    def get(self, request):
        veiculo = Veiculo.objects.all()
        serializer = VeiculoSerializer(veiculo, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = VeiculoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#class CRUD Veiculo (DELETE/PUT)
class crudVeiculoESTGDAPIView(APIView):
        def delete(self, request, pk):
            veiculo = get_object_or_404(Pedido, pk=pk, user=request.user)
            veiculo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        def put(self, request, pk):
            veiculo = get_object_or_404(Veiculo, pk=pk)
            serializer = VeiculoSerializer(veiculo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API Lista Utilizadores
class ListUtilizadorESTGDAPIView(APIView):
        def get(self, request):
            utilizador = User.objects.all()
            serializer = UserSerializer(utilizador, many=True)
            return Response(serializer.data)

        def post(self, request):
            request.data['user'] = request.user.id
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#Class CRUD utilizador (DELETE/PUT)
class crudUtilizadorESTGDAPIView(APIView):
        def delete(self, request, pk):
            utilizador = get_object_or_404(User, pk=pk)
            utilizador.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        def put(self, request, pk):
            utilizador = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(User, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Class Login de utilizador
class LoginView(APIView):

    def post(request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            username = serializer.validated_data['username']

            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user:

                token, created = Token.objects.get_or_create(user=user)

                return Response({'token': token.key})

            else:

                return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)