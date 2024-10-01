from db.connectionmongo import db
from db.connectionredis import rediscon
from cruds.compra import listar_produtos
import pprint
from bson import ObjectId

printer = pprint.PrettyPrinter(indent=2)

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