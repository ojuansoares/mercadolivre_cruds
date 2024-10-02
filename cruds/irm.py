from db.connectionmongo import db
from db.connectionredis import rediscon
from cruds.compra import listar_produtos, verificar_existencia
from cruds.login import verificar_usuario_logado
import pprint
from bson import ObjectId
import json

printer = pprint.PrettyPrinter(indent=2)

# ----- INÍCIO IMPLEMENTAÇÃO PRODUTO (REDIS/MONGO) -----

def verificar_existencia_produtos():
    produtos_count = db.produto.count_documents({})
    if produtos_count == 0:
        print()
        print("Não existem produtos cadastrados.")
        return False
    return True

def sincronizacao_redis():
    mycol = db.produto
    produtos = list(mycol.find())
    for produto in produtos:
        rediscon.set(f"produto:{produto['nome']}", produto['valor'])
    return

def listar_produtos_redis():
    produtos = rediscon.keys("produto:*")
    for produto in produtos:
        valor = rediscon.get(produto).decode('utf-8')
        print(f"Produto: {produto.decode('utf-8')}, Valor: {valor}")

def soma_100_produtos():
    produtos = rediscon.keys("produto:*")
    for produto in produtos:
        valor = float(rediscon.get(produto).decode('utf-8'))
        novo_valor = valor + 100
        rediscon.set(produto, novo_valor)
        print(f"Produto: {produto.decode('utf-8')}, Novo Valor: {novo_valor}")

def deletar_produtos_redis():
    produtos = rediscon.keys("produto:*")
    for produto in produtos:
        rediscon.delete(produto)
    return

def sincronizacao_mongo():
    mycol = db.produto
    produtos = rediscon.keys("produto:*")

    for produto in produtos:
        nome = produto.decode('utf-8').replace("produto:", "")
        valor = float(rediscon.get(produto).decode('utf-8'))
        myquery = {"nome": nome}
        newvalues = {"$set": {"valor": valor}}

        mycol.update_one(myquery, newvalues)
        print(f"Produto {nome} sincronizado com sucesso!")

def create_produto_redis():
    mycol = db.produto

    while True:
        nome = input("Nome do produto: ")
        if mycol.find_one({"nome": nome}):
            print("Produto com esse nome já existe!")
            continue
        else:
            break

    while True:
        descricao = input("Descrição do produto: ")
        if descricao:
            break
        else:
            print("Descrição é um campo obrigatório.")

    while True:
        valor = input("Valor do produto: ")
        try:
            valor = float(valor)
            break
        except ValueError:
            print("Valor inválido. Digite um número.")

    print("Escolha o dono do produto pelo indice:")
    vendedores = list(db.vendedor.find())
    for idx, vendedor in enumerate(vendedores):
        print(f"{idx} - {vendedor['nome']} {vendedor['sobrenome']}")

    while True:
        try:
            indice = int(input("Digite o índice do vendedor: "))
            if 0 <= indice < len(vendedores):
                break
            else:
                print("Índice inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    id_dono = vendedores[indice]["_id"]
    nome_dono = vendedores[indice]["nome"]
    email_dono = vendedores[indice]["email"]

    produto = {
        "descricao": descricao,
        "valor": str(valor),
        "id_dono": str(id_dono),
        "nome_dono": nome_dono,
        "email_dono": email_dono,
        "comentarios": "[]"
    }
    rediscon.hmset(f"produto:{nome}", produto)
    print()
    print("Produto criado com sucesso no Redis!")

    sincronizar_novo_produto(nome)


def sincronizar_novo_produto(nome_produto):
    produto_redis = rediscon.hgetall(f"produto:{nome_produto}")

    produto_mongo = {
        "nome": nome_produto,
        "descricao": produto_redis[b'descricao'].decode('utf-8'),
        "valor": float(produto_redis[b'valor'].decode('utf-8')),
        "id_dono": {"id_dono": ObjectId(produto_redis[b'id_dono'].decode('utf-8'))},
        "nome_dono": {"nome_dono": produto_redis[b'nome_dono'].decode('utf-8')},
        "email_dono": {"email_dono": produto_redis[b'email_dono'].decode('utf-8')},
        "comentarios": []
    }

    db.produto.insert_one(produto_mongo)
    print(f"Produto {nome_produto} sincronizado com sucesso do Redis para o MongoDB!")

    rediscon.delete(f"produto:{nome_produto}")

# ----- FIM DA IMPLEMENTAÇÃO PRODUTO (REDIS/MONGO) -----

# ----- INÍCIO IMPLEMENTAÇÃO FAVORITOS (REDIS/MONGO) -----

def adicionar_favorito_redis():
    if not verificar_existencia():
            return
    
    usuario = db.usuario.find_one({"email": verificar_usuario_logado()})

    if not verificar_existencia_cache():
        criar_cache_favoritos()

    print()
    listar_produtos()
    while True:
        produto_nome = input("Nome do produto que deseja favoritar: ")
        produto = db.produto.find_one({"nome": produto_nome})
        if not produto:
            print("Produto não encontrado.")
            continue
        else:
            break
    
    favorito = {
        "nome": produto["nome"],
        "descricao": produto["descricao"],
        "valor": produto["valor"]
    }

    favoritos_str = rediscon.get(f"{usuario['cpf']}")
    if favoritos_str:
        favoritos = json.loads(favoritos_str.decode('utf-8'))
    else:
        favoritos = []

    favoritos.append(favorito)
    rediscon.set(f"{usuario['cpf']}", json.dumps(favoritos))
    print("Favorito adicionado ao cache do Redis com sucesso!")

def remover_favorito_redis():
    print()
    usuario = db.usuario.find_one({"email": verificar_usuario_logado()})
    if not usuario.get("favoritos"):
        print("Usuário não possui favoritos.")
        return
    
    if not verificar_existencia_cache():
        criar_cache_favoritos()
    
    print("Favoritos do usuário:")
    favoritos_str = rediscon.get(f"{usuario['cpf']}")
    favoritos = json.loads(favoritos_str.decode('utf-8'))
    for i, favorito in enumerate(favoritos):
        print(f"{i}: Nome: {favorito['nome']}, Descrição: {favorito['descricao']}, Valor: {favorito['valor']}")
    
    indice = input("Digite o índice do favorito que deseja remover: ")
    
    if indice.isdigit() and int(indice) < len(favoritos):
        indice = int(indice)
        favoritos.pop(indice)
        rediscon.set(f"{usuario['cpf']}", json.dumps(favoritos))
        print("Favorito removido com sucesso!")
    else:
        print("Índice inválido ou nenhum favorito selecionado. Nenhuma alteração feita.")

def listar_favoritos_redis():
    usuario = db.usuario.find_one({"email": verificar_usuario_logado()})
    if not usuario.get("favoritos"):
        print()
        print("Usuário não possui favoritos.")
        return
    
    if not verificar_existencia_cache():
        criar_cache_favoritos()
    
    print()
    print("Favoritos do usuário:")
    favoritos_str = rediscon.get(f"{usuario['cpf']}")
    favoritos = json.loads(favoritos_str.decode('utf-8'))
    for i, favorito in enumerate(favoritos):
        print(f"{i}: Nome: {favorito['nome']}, Descrição: {favorito['descricao']}, Valor: {favorito['valor']}")
   
def sincronizar_favoritos():
    print()
    if not verificar_existencia_cache():
        print("Não há o que sincronizar!")
        return

    usuario = db.usuario.find_one({"email": verificar_usuario_logado()})
    mycol = db.usuario
    myquery = {"cpf": usuario['cpf']}

    favoritos_str = rediscon.get(f"{usuario['cpf']}")
    favoritos = json.loads(favoritos_str.decode('utf-8'))
    newvalues = { "$set": {"favoritos": favoritos} }

    print("Sincronização Com o MongoDB Realizada com Sucesso!")

    mycol.update_one(myquery, newvalues)
    deletar_cache_favoritos()

def criar_cache_favoritos():
    usuario = db.usuario.find_one({"email": verificar_usuario_logado()})
    favoritos_usuario = usuario["favoritos"]
    rediscon.set(f"{usuario["cpf"]}", json.dumps(favoritos_usuario))
    print("Favoritos sincronizados ao redis com sucesso!")

def deletar_cache_favoritos():
    usuario = db.usuario.find_one({"email": verificar_usuario_logado()})
    rediscon.delete(f"{usuario["cpf"]}")

def verificar_existencia_cache():
    usuario = db.usuario.find_one({"email": verificar_usuario_logado()})
    
    if rediscon.exists(f"{usuario["cpf"]}"):
        return True
    else:
        return False

# ----- FIM IMPLEMENTAÇÃO FAVORITOS (REDIS/MONGO) -----

# ----- EXECUÇÃO DA IMPLEMENTAÇÃO PRODUTOS (REDIS/MONGO) -----

def irm():
    if not verificar_existencia_produtos():
        return
    
    print()
    print("Sincronizando Produtos para o Redis...")
    sincronizacao_redis()
    print("Produtos sincronizados com sucesso!")

    print()
    listar_produtos()

    print()
    print("Somando 100 em cada produto do Redis:")
    soma_100_produtos()

    print()
    print("Sincronizando Produtos para o Mongo:")
    sincronizacao_mongo()
    print()

    deletar_produtos_redis()

    print("Produtos Sincronizados com Sucesso!")