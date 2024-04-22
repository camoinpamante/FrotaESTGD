
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Veiculo, User, Pedido


# Create your views here.

def home(request):
    if request.user.is_authenticated:
       veiculos = Veiculo.objects.all()
       return render(request, 'home.html', {'veiculos': veiculos})
    else:
        return redirect('login')


def login_app(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return render(request, 'home.html',{'user': user})
    return render(request, 'log.html')

def logout_app(request):
    logout(request)

    return redirect('login')

def registerDepartamento(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        departamento = Departamento(nome =nome)
        departamento.save()
        return HttpResponse('Dados registrados com sucesso!')
    else:
        return render(request, 'departamento.html')
def about(request):
    return render(request, 'about.html')

def veiculoregister(request):
    if request.method == 'POST':
        marca = request.POST.get('marca')
        tipo_combustivel = request.POST.get('tipo_combustivel')
        matricula = request.POST.get('matricula')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        veiculo = Veiculo(marca = marca, tipo_combustivel = tipo_combustivel, matricula = matricula, description = description, image = image)
        veiculo.save()
        return HttpResponse('Veiculo registrado com sucesso! ')
    else:
        return render(request, 'veiculos.html')

def listveiculos(request):
    veiculos = Veiculo.objects.all()
    return render(request, 'listveiculos.html', {'veiculos':veiculos})

def registeruser(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email= request.POST.get('email')
        password1= request.POST.get('password1')
        if password1==password:
            user= User(username = username, password = password, email = email, first_name = firstname, last_name = lastname)
            if user is not None:
               user.save()
               login(request, user)
               messages.success(request, 'Utilizador criado com sucesso!')
               return redirect('home')

            else:
                messages.success(request, " Erro ao criar utilizador!!")
                return render(request, 'createUser.html')
        else:
            messages.success(request, "As senhas devem ser iguais.")
            return render(request, 'createUser.html')
    else:
        return render(request, 'createUser.html')

def fazerpedido(request, id):

    return render(request, 'pedidoVeiculo.html')


def registarpedido(request, veiculo_id):

    if request.method == 'POST':
        veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
        user = request.user.id
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        local= request.POST.get('local')
        combustivel_inicial = request.POST.get('combustivel_inicial')
        combustivel_fim = request.POST.get('combustivel_fim')
        kilometro_inicial = request.POST.get('kilometro_inicial')
        kilometro_final= request.POST.get('kilometro_final')
        pedido = Pedido(user=user, veiculo=veiculo ,data_inicio = data_inicio, data_fim = data_fim, local =local,
                        combustivel_inicial =combustivel_inicial,combustivel_fim = combustivel_fim,
                        kilometro_inicial = kilometro_inicial, kilometro_final =kilometro_final)

        if pedido is not None:
            pedido.save()
            messages.success(request, 'Pedido registrado com sucesso!')
            return redirect('home')
        else:
            messages.error('erro ao registrar pedido')
            return redirect('fazerpedido')
    return redirect('fazerpedido')

def veiculoList(request):
    veiculos = Veiculo.objects.all()
    return render(request, 'veiculoList.html', {'veiculos':veiculos})

def userList(request):
    users = User.objects.all()
    return render(request, 'userList.html', {'users':users})

def pedidoList(request):
    pedido = User.objects.all()
    return render(request, 'pedidoList.html', {'pedidos':pedido})

def eliminarveiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    veiculo.delete()
    messages.success(request, 'Veiculo eliminado com sucesso!!')
    return redirect('veiculoList')

def eliminaruser(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, 'Utilizador eliminado com sucesso!!')
    return redirect('userList')

def editarveiculo(request, pk):
    veiculos = get_object_or_404(Veiculo, pk=pk)

    return render(request, 'editarveiculo.html', {'veiculo': veiculos})
def editaruser(request, pk):
    user = get_object_or_404(User, pk=pk)

    return render(request, 'editaruser.html', {'user': user})

def veiculoeditado(request, pk):
    veiculo = get_object_or_404(Veiculo, id=pk)
    if request.method == 'POST':
        marca = request.POST.get('marca')
        tipo_combustivel = request.POST.get('tipo_combustivel')
        matricula = request.POST.get('matricula')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        veiculo = Veiculo(pk=pk,marca=marca, tipo_combustivel=tipo_combustivel, matricula=matricula, description=description,
                          image=image)
        veiculo.save()
        return HttpResponse('Veiculo alterado com sucesso! ')
    else:
        messages.success(request, 'Erro na alteração de veiculo!')
        return redirect('listarveiculo')

def usereditado(request, pk):
    user = User.objects.get(id=pk)
    if user is not None:
            if request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                email = request.POST.get('email')
                password1 = request.POST.get('password1')
                if password1 == password:
                    user = User(pk= pk, username=username, password=password, email=email)
                    if user is not None:
                        user.save()
                        login(request, user)
                        messages.success(request, 'Utilizador alterado com sucesso!')
                        return redirect('userList')

                    else:
                        messages.success(request, " Erro ao alterar utilizador!!")
                        return render(request, 'userList.html')
                else:
                    messages.success(request, "As senhas devem ser iguais.")
                    return render(request, 'userList.html')
            else:
                messages.success(request, "Erro POSt.")
                return render(request, 'userList.html')
    else:
        messages.success(request, "Erro ao alterar.")
        return render(request, 'userList.html')