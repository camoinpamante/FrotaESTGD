from contextvars import Token

from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import  APIView
from .serializers import VeiculoSerializer, PedidoSerializer, UserSerializer, LoginSerializer
from frota.models import Veiculo, Pedido, User


# Create your views here.
class ListESTGDAPIView(APIView):
    '''Lista todos os pedidos e inserção'''
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

class crudESTGDAPIView(APIView):
    '''Altera e exclui os pedidos do veiculo'''
    def delete(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk, user=request.user)
        pedido.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk, user=request.user)
        serializer = PedidoSerializer(pedido,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListVeiculoESTGDAPIView(APIView):
    ''' Lista todos os veiculos e regista um novo veiculo '''
    def get(self, request):
        veiculo = Veiculo.objects.all()
        serializer = VeiculoSerializer(veiculo, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = VeiculoSerializer(data=request.data, files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class crudVeiculoESTGDAPIView(APIView):
        '''Alteração e exclusão dos veiculos'''
        def delete(self, request, pk):
            veiculo = get_object_or_404(Pedido, pk=pk, user=request.user)
            veiculo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        def put(self, request, pk):
            veiculo = get_object_or_404(Veiculo, pk=pk)
            serializer = VeiculoSerializer(veiculo, data=request.data, files=request.FILES)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API Lista Utilizadores
class ListUtilizadorESTGDAPIView(APIView):
        '''Lista todos os utilizadores e registat um novo utilizador'''

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

class crudUtilizadorESTGDAPIView(APIView):
        '''Alteração e exclusão de utilizadores'''
        def delete(self, request, pk):
            utilizador = get_object_or_404(User, pk=pk)
            utilizador.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        def put(self, request, pk):
            utilizador = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(utilizador, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


