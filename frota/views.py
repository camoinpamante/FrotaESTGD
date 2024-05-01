import smtplib

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q


from .models import Veiculo, User, Pedido, Notification


# Create your views here.

def home(request):
    try:
        ''' Verificação de login -para ter acesso a página web tens que ser logado. '''
        if request.user.is_authenticated:
           veiculos = Veiculo.objects.all()
           return render(request, 'home.html', {'veiculos': veiculos})
        else:
            return redirect('login')
    except:
        messages.success(request, 'Erro do sistema!')
        return redirect('login')



def login_app(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'log.html')
    except:
        messages.success(request, 'Erro do sistema!')
        return redirect('login')

def logout_app(request):
    logout(request)
    return redirect('index')


def about(request):
    return render(request, 'about.html')

def veiculoregister(request):
    try:
        if request.method == 'POST':
            marca = request.POST.get('marca')
            tipo_combustivel = request.POST.get('tipo_combustivel')
            matricula = request.POST.get('matricula')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            veiculo = Veiculo(marca = marca, tipo_combustivel = tipo_combustivel, matricula = matricula, description = description, image = image)
            veiculo.save()
            messages.success(request, 'Veiculo registrado com sucesso! ')
            return redirect('veiculoList')
        else:
            return render(request, 'veiculos.html')
    except:
        messages.success(request, 'Erro do sistema!')
        return redirect('veiculos.html')

def listveiculos(request):
    veiculos = Veiculo.objects.all()
    return render(request, 'listveiculos.html', {'veiculos':veiculos})

def register(request):
    return render(request, 'createUser.html')

def registeruseradmin(request):
    return render(request, 'createUseradmin.html')
def registeruser(request):
    try:

            if request.method == 'POST':
                username= request.POST.get('username')
                password= request.POST.get('password')
                email= request.POST.get('email')
                firstname = request.POST.get('firstname')
                lastname = request.POST.get('lastname')
                password1= request.POST.get('password1')
                if password1==password:
                    hashed_password = make_password(password)
                    print(f"Original Password: ",password)
                    print(f"Hashed Password:", hashed_password)
                    user= User(username = username, password = hashed_password, email = email, first_name = firstname, last_name =lastname)
                    if user is not None:

                       user.save()
                       if request.user.is_authenticated:
                           messages.success(request, 'Utilizador criado com sucesso!')
                           return render(request, 'log.html')
                       else:
                           return redirect('login')
                    else:
                        messages.success(request, " Erro ao criar utilizador!!")
                        return render(request, 'createUser.html')
                else:
                    messages.success(request, "As senhas devem ser iguais.")
                    return render(request, 'createUser.html')
            else:
                return render(request, 'createUser.html')
    except:
        if request.user.is_authenticated:
            messages.success(request, 'Erro do sistema!')
            return redirect('userList')
        else:
            messages.success(request, 'Erro do sistema!')
            return redirect('login')



def fazerpedido(request,veiculo_id, id_user):
    try:
        veiculo = Veiculo.objects.get(pk=veiculo_id)
        user = User.objects.get(pk=id_user)
        return render(request, 'pedidoVeiculo.html',{'veiculo':veiculo, 'user':user})
    except:
        messages.success(request, 'Erro inesperado!')
        return redirect('home')


def registarpedido(request, veiculo_id):
    try:
        veiculo_id  = get_object_or_404(Veiculo, pk=veiculo_id)
        if request.method == 'POST':
            veiculo_id = request.POST.get('veiculo')
            veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
            data_inicio = request.POST.get('data_inicio')
            data_fim = request.POST.get('data_fim')
            local= request.POST.get('local')
            combustivel_inicial = request.POST.get('combustivel_inicial')
            combustivel_fim = request.POST.get('combustivel_fim')
            kilometro_inicial = request.POST.get('kilometro_inicial')
            kilometro_final= request.POST.get('kilometro_final')
            pedido = Pedido(user=request.user, veiculo=veiculo ,data_inicio = data_inicio, data_fim = data_fim, local =local,
                            combustivel_inicial =combustivel_inicial,combustivel_fim = combustivel_fim,
                            kilometro_inicial = kilometro_inicial, kilometro_final =kilometro_final)
            nome = request.user.username
            ''' Caso o pedido não é vazio envia a notificação para administrador '''
            if pedido is not None:
                pedido.save()
                funcionario ="admin"
                mensagem = "O funcionario "+ nome +" fez pedido do veiculo com destino à "+ local
                notificacao = Notification(user=pedido.user, funcionario=funcionario, mensagem=mensagem,confirmacao=False)
                notificacao.save()
                messages.success(request, 'Pedido registrado com sucesso!')
                return redirect('home')
            else:
                messages.error('erro ao registrar pedido')
                return redirect('fazerpedido')
        return redirect('fazerpedido')
    except:
        messages.success(request, 'Erro inesperado!')
        return redirect('home')

def veiculoList(request):
    try:
        veiculos = Veiculo.objects.all()
        return render(request, 'veiculoList.html', {'veiculos':veiculos})
    except:
        messages.success(request, 'Erro o sistema não consegue carregar os dados!')
        return redirect('home')

def userList(request):
    try:
        users = User.objects.all()
        return render(request, 'userList.html', {'users': users})
    except:
        messages.success(request, 'Erro o sistema não consegue carregar os dados!')
        return redirect('home')

def find(request):
    try:
        if request.method == 'GET':
            pesq = request.GET['foo']
            q = get_object_or_404(User, username=pesq)
            '''Verifica se o pedido existe na base de dados se não retorna a lista completa'''
            if q is not None:
                users = User.objects.filter(username=q.username)
                if users is not None:
                  return render(request, 'userList.html', {'users': users})
                elif users is None:
                  d= User.objects.all()
                  return render(request, 'userList.html', {'users': d})
            else:
                d = User.objects.all()
                return render(request, 'userList.html', {'users': d})
    except:
        messages.success(request, 'Erro o sistema não consegue carregar os dados!')
        return redirect('userList')

def findPedido(request):

        if request.method == 'GET':
            pesq = request.GET['pedido']
            pedidos = Pedido.objects.filter(user=pesq)
            q = get_object_or_404(Pedido, pk=pedidos.id)
            if q is not None:

                if pedidos is not None:
                  return render(request, 'pedidoList.html', {'pedidos': pedidos})
                elif pedidos is None:
                  d= Pedido.objects.all()
                  return render(request, 'pedidoList.html', {'pedidos': d})
            else:
                d = Pedido.objects.all()
                return render(request, 'pedidoList.html', {'pedidos': d})


def pesquisarVeiculo(request):
    try:
        if request.method == 'GET':
            mar = request.GET['marca']
            marca = get_object_or_404(Veiculo, marca= mar)
            if marca is not None:
                veiculos = Veiculo.objects.filter(marca=marca)
                if veiculos is not None:
                  return render(request, 'veiculoList.html', {'veiculos':veiculos})
                elif veiculos is None:
                  k= Veiculo.objects.all()
                  return render(request, 'veiculoList.html', {'veiculos':k})
            else:
                k = Veiculo.objects.all()
                return render(request, 'veiculoList.html', {'veiculos':k})
    except:
        messages.success(request, 'Erro o sistema não consegue carregar os dados!')
        return  redirect('veiculoList')
def pedidoList(request):
    try:
        pedido = Pedido.objects.filter(confirmacao=Pedido.confirmacao=='False')
        return render(request, 'pedidoList.html', {'pedidos':pedido})
    except:
        messages.success(request, 'Erro o sistema não consegue carregar os dados!')
        return redirect('home')

def pedidorejeitadoList(request):
    try:
        pedido = Pedido.objects.filter(confirmacao=Pedido.confirmacao !='False')
        return render(request, 'pedidoConfirmList.html', {'pedidos':pedido})
    except:
        messages.success(request, 'Erro o sistema não consegue carregar os dados!')
        return redirect('home')

def eliminarveiculo(request, pk):
    try:
        veiculo = get_object_or_404(Veiculo, pk=pk)
        veiculo.delete()
        messages.success(request, 'Veiculo eliminado com sucesso!!')
        return redirect('veiculoList')
    except:
        messages.success(request, 'Erro inesperado!')
        return redirect('veiculoList')
def eliminarpedido(request, pk):
    try:
        pedido = get_object_or_404(Pedido, pk=pk)
        pedido.delete()
        messages.success(request, 'pedido eliminado com sucesso!!')
        return redirect('pedidoList')
    except:
        messages.success(request, 'Erro inesperado!')
        return redirect('pedidoList')

def eliminarnotificacao(request, pk):
    try:
        notificacao = get_object_or_404(Notification, pk=pk)
        notificacao.delete()
        messages.success(request, 'Notificacao eliminado com sucesso!!')
        return redirect('home')
    except:
        messages.success(request, 'Erro inesperado!')
        return redirect('home')
def eliminaruser(request, pk):
    try:
        user = get_object_or_404(User, pk=pk)
        user.delete()
        messages.success(request, 'Utilizador eliminado com sucesso!!')
        return redirect('userList')
    except:
        messages.success(request, 'Erro inesperado!')
        return redirect('userList')

def editarveiculo(request, pk):
    try:
        veiculos = get_object_or_404(Veiculo, pk=pk)
        return render(request, 'editarveiculo.html', {'veiculo': veiculos})
    except:
        messages.success(request, 'Erro inesperado!')
        return redirect('veiculoList')
def editarpedido(request, pk):
    try:
        pedidos = get_object_or_404(Veiculo, pk=pk)

        return render(request, 'editarpedido.html', {'pedido': pedidos})
    except:
        messages.success(request, 'Erro inesperado!')
        return redirect('pedidoList')
def editaruser(request, pk):
    try:
        user = get_object_or_404(User, pk=pk)
        return render(request, 'editaruser.html', {'user': user})
    except:
        messages.success(request, 'Erro inesperado!')
        return redirect('userList')

def pedidoeditado(request, pk):
    try:
            pedido = get_object_or_404(Veiculo, id=pk)
            if request.method == 'POST':
                veiculo_id = request.POST.get('veiculo')
                veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
                data_inicio = request.POST.get('data_inicio')
                data_fim = request.POST.get('data_fim')
                local = request.POST.get('local')
                combustivel_inicial = request.POST.get('combustivel_inicial')
                combustivel_fim = request.POST.get('combustivel_fim')
                kilometro_inicial = request.POST.get('kilometro_inicial')
                kilometro_final = request.POST.get('kilometro_final')
                pedido = Pedido(user=request.user, veiculo=veiculo, data_inicio=data_inicio, data_fim=data_fim, local=local,
                                combustivel_inicial=combustivel_inicial, combustivel_fim=combustivel_fim,
                                kilometro_inicial=kilometro_inicial, kilometro_final=kilometro_final)

                if pedido is not None:
                    pedido.save()
                    messages.success(request, 'Pedido registrado com sucesso!')
                    return redirect('pedidoList')
                else:
                    messages.success(request, 'Erro ao alterar o pedido!')
                    return redirect('home')
    except:
        messages.success(request, 'Erro ao alterar o pedido!')
        return redirect('home')

def veiculoeditado(request, pk):
    try:
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
                messages.success(request, 'Veiculo alterar com sucesso')
                return redirect('veiculoList')
            else:
                messages.success(request, 'Erro ao alterar veiculo')
                return render(request, 'veiculoList')
    except:
        messages.success(request, 'Erro ao alterar veiculo')
        return render(request, 'veiculoList')

def usereditado(request, pk):
    try:
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
    except:
        messages.success(request, "Erro ao alterar.")
        return render(request, 'userList.html')


def confirmar(request, pedido_id):
  try:
         pedido = get_object_or_404(Pedido, pk=pedido_id)
         '''Mudar estado do pedido para confirmado'''
         pedido.confirmacao= not pedido.confirmacao
         '''Envia a notificação ao utilizador'''
         funcionario = pedido.user.username
         mensagem = "O seu pedido foi autorizado !!"
         notificacao = Notification(user= pedido.user,funcionario= funcionario, mensagem=mensagem, confirmacao = False)
         notificacao.save()
         messages.success(request, "Notificação foi enviada ao funcionário. ")
         pedido.save()
         return redirect('pedidoList')
  except:
      messages.success(request, "Erro na confirmação do pedido. ")
      return redirect('pedidoList')




def notificacao(request, pk):
    '''Muda o estado da notificação e elimina da lista'''
    try:
      notificacao = get_object_or_404(Notification, funcionario=pk)
      messages.success(request, "O seu pedido foi autorizado !!")

      notificacao.confirmacao = not notificacao.confirmacao
      notificacao.delete()
      return redirect('home')
    except:
      messages.success(request,  'Notificação vazia !!')
      return redirect('home')

def notificationsadmin(request, funcionario):
    '''Lista notificações do admin'''
    try:
        notificacoes = Notification.objects.filter(funcionario=funcionario)
        return render(request, 'notificationList.html', {'notificacoes':notificacoes})
    except:
        messages.success(request, 'Erro o sistema não consegue carregar os dados!')
        return redirect('home')