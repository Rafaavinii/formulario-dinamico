import re
from django.contrib.auth.models import User

def validar_senha(senha):
    # Comprimento mínimo de 8 caracteres
    mensagens_erro = []
    if len(senha) < 8:
        mensagens_erro.append('A senha deve ter pelo menos 8 caracteres.')

    # Pelo menos uma letra maiúscula
    if not re.search(r'[A-Z]', senha):
        mensagens_erro.append('A senha deve conter pelo menos uma letra maiúscula.')

    # Pelo menos uma letra minúscula
    if not re.search(r'[a-z]', senha):
        mensagens_erro.append('A senha deve conter pelo menos uma letra minúscula.')

    # Pelo menos um número
    if not re.search(r'[0-9]', senha):
        mensagens_erro.append('A senha deve conter pelo menos um número.')

    return mensagens_erro

def validar_email(email):

    jah_exist = User.objects.filter(email=email).exists()
    # Padrão de expressão regular para validar o formato do e-mail
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    erro = []
    
    # # Verifica se o e-mail corresponde ao padrão
    # if re.match(padrao, email):
    #     erro.append('Email inválido.')
    # elif jah_exist:
    #     erro.append('Email já cadastrado.')

    return erro


