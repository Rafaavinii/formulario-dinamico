from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from formulario.models import FormDinamico

from user.validators import validar_email, validar_senha

def cadastro_view(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirm_senha = request.POST.get('confirm_senha')

        if senha != confirm_senha:
            print(senha, confirm_senha)
            messages.error(request, 'As senha não coincidem.')
            return render(request, 'cadastro.html')

        if len(validar_senha(senha)) != 0:
            for erro in validar_senha(senha):
                messages.error(request, erro)
            return render(request, 'cadastro.html')
        
        if len(validar_email(email)) != 0:
            erros = validar_email(email)
            for erro in erros:
                messages.error(request, erro)
            return render(request, 'cadastro.html')
    
        User.objects.create_user(
            first_name = nome,
            last_name = sobrenome,
            username=email,
            email=email,
            password=senha
        )

        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('entrar')


def entrar_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = authenticate(request, username=email, password=senha)

        if user is not None:
            login(request, user)
            return redirect('pagina_inicial')
        
        else:
            messages.error(request, 'Email ou Senha incorretos.')
            return render(request, 'login.html')

def logout_view(request):
    # logout do candidato
    logout(request)
    return redirect('pagina_inicial')

@login_required
def dashboard_view(request):
    if request.method == 'GET':
        context = {}

        user = request.user

        usuario = User.objects.get(id=user.id)
        formularios = FormDinamico.objects.filter(user_id=user.id)

        lista_formulario = []
        for formulario in formularios:
            dicionario = {
                'nome': formulario.nome,
                'descricao': formulario.descricao,
                'data': formulario.data_criacao,
            }
            lista_formulario.append(dicionario)

        context['nome'] = usuario.first_name
        context['sobrenome'] = usuario.last_name
        context['email'] = usuario.email
        context['quantidade_formulario'] = formularios.count()
        context['formularios'] = lista_formulario

        print(context['formularios'])

        return render(request, 'pagina_inicial.html', context)