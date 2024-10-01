from db.connectionredis import rediscon
from cruds.usuario import get_user_by_email

def login(email, senha):
    user = get_user_by_email(email)
    if not user:
        print("Usuário não encontrado.")
        return False
    
    if user["senha"] == senha:
        rediscon.setex(f"user:{email}", 120, email)
        print(f"Usuário {email} logado com sucesso!")
        return True
    else:
        print("Senha incorreta.")
        return False

def verificar_usuario_logado():
    usuario_logado = None
    chaves = rediscon.keys("user:*")
    
    if chaves:
        chave = chaves[0]
        usuario_logado = rediscon.get(chave).decode('utf-8')
        return usuario_logado
    else:
        return False

def verificar_e_expirar_login():
    usuario_logado = rediscon.keys("user:*")
    
    if not usuario_logado:
        print()
        print("O login expirou ou não há usuário logado.")
        return False
    else:
        return True

def logout():

    usuario_logado = verificar_usuario_logado()

    rediscon.delete(f"user:{usuario_logado}")
    print()
    print(f"Usuário {usuario_logado} deslogado manualmente.")
