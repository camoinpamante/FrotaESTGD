from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.views import APIView, status
from frota.models import Veiculos, Pedido, User

from .serializers import VeiculoSerializer, PedidoSerializer
from ..frota.models import Veiculo


# Create your views here.

# Create your views here.
class ESTGDAPIView(APIView):
    def get(self, request):
        pedido = Pedido.objects.all()
        serializer = PedidoSerializer(pedido, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_pedido):
        pedido = get_object_or_404(Pedido, pk=id_pedido, user=request.user.id)
        pedido.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request,id_pedido):
        pedido = get_object_or_404(Pedido, pk=id_pedido, user=request.user.id)
        serializer = PedidoSerializer(pedido,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class VeiculoAPIView(APIView):
    def get(self, request, pk=None):
        veiculo = get_object_or_404(Veiculo, pk=pk, user=request.user)
        serializer = VeiculoSerializer(veiculo, many=False)
        return Response(serializer.data)

    def put(self, request, pk=None):
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
