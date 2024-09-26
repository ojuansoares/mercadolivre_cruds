# redis/login.py

from db.connectionredis import rediscon
from cruds.usuario import get_user_by_email

# Função para logar o usuário com expiração de 2 minutos
def login(email, senha):
    user = get_user_by_email(email)  # Função existente no MongoDB que obtém o usuário
    if not user:
        print("Usuário não encontrado.")
        return False
    
    if user["senha"] == senha:
        # Guardar o email do usuário no Redis com expiração de 300 segundos
        rediscon.setex(f"user:{email}", 120, email)
        print(f"Usuário {email} logado com sucesso!")
        return True
    else:
        print("Senha incorreta.")
        return False

# Função para verificar se há um usuário logado
def verificar_usuario_logado():
    usuario_logado = None
    chaves = rediscon.keys("user:*")
    
    if chaves:
        chave = chaves[0]
        usuario_logado = rediscon.get(chave).decode('utf-8')
        return usuario_logado
    else:
        return False

# Função para verificar se o login ainda é válido
def verificar_e_expirar_login():
    # Buscar a chave que representa o login do usuário
    usuario_logado = rediscon.keys("user:*")
    
    if not usuario_logado:
        print("O login expirou ou não há usuário logado.")
        return False
    else:
        return True

# Função para logout manual
def logout():

    usuario_logado = verificar_usuario_logado()

    rediscon.delete(f"user:{usuario_logado}")
    print(f"Usuário {usuario_logado} deslogado manualmente.")
