
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import  Veiculo, User


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
        email= request.POST.get('email')
        password1= request.POST.get('password1')
        if password1==password:
            user= User(username = username, password = password, email = email)
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

