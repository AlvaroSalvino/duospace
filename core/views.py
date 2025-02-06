from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from perfil.models import *

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        login_input = request.POST.get('username')  # Pode ser tanto o username quanto o email
        password = request.POST.get('password')
        
        # Tentar obter o usuário com base no login (username ou email)
        user = None
        if '@' in login_input:
            # Se o input contém "@", assumimos que é um email
            try:
                user = User.objects.get(email=login_input)
            except User.DoesNotExist:
                user = None
        else:
            # Caso contrário, tentamos como username
            user = User.objects.filter(username=login_input).first()
        
        # Autenticar o usuário
        if user is not None:
            user = authenticate(request, username=user.username, password=password)
        
        if user is not None:
            # Se o usuário foi autenticado corretamente, fazer login
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    # Renderizar o novo template login.html
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def inscrevase(request):
    if request.method == 'POST':
        nome_completo = request.POST.get('login-nome')
        nomes = nome_completo.split()

        # Tratar o caso em que o nome pode ter mais de um sobrenome
        nome = nomes[0]
        sobrenome = ' '.join(nomes[1:])  # Considera todos os nomes após o primeiro como sobrenome
        ultimo_nome = nomes[-1]
        email = request.POST.get('login-email')

        # Criação do username com base no primeiro nome e último nome
        username = f"{nome}.{ultimo_nome}"

        # Verificar se o username já existe, e se existir, adicionar um número
        if User.objects.filter(username=username).exists():
            contador = 1
            while User.objects.filter(username=f"{username}{contador}").exists():
                contador += 1
            username = f"{username}{contador}"

        senha = request.POST.get('password')  # Ajuste aqui para corresponder ao campo do template
        telefone_perfil = request.POST.get('login-telefone')

        if User.objects.filter(username=username).exists():
            context = {'erro': 'Usuário já cadastrado no sistema!'}
            return render(request, 'registration/inscreva-se.html', context)

        try:
            # Criação do usuário Django
            user = User.objects.create_user(
                username=username,
                first_name=nome,
                last_name=sobrenome,
                email=email
            )
            # Atribui a senha com set_password para garantir segurança
            user.set_password(senha)
            user.save()

            # Criação do perfil
            perfil = Perfil(nome=username,
                            telefone=telefone_perfil,
                            usuario=user)
            perfil.save()

            # Redirecionar após sucesso
            return redirect('login')  # Redireciona para a página de login (ajuste o nome da URL conforme necessário)

        except Exception as e:
            context = {'erro': 'Erro ao criar o usuário!'}
            return render(request, 'registration/inscreva-se.html', context)

    return render(request, 'registration/inscreva-se.html', {})

