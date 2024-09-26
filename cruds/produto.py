from db.connectionmongo import db
import pprint

printer = pprint.PrettyPrinter(indent=2)

def create_produto():
    mycol = db.produto
    mycol_vendedores = db.vendedor

    if mycol_vendedores.count_documents({}) == 0:
        print("Não há vendedores cadastrados. Cadastre um vendedor antes de criar um produto.")
        return

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
    vendedores = list(mycol_vendedores.find())
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
        "nome": nome,
        "descricao": descricao,
        "valor": valor,
        "id_dono": {"id_dono": id_dono},
        "nome_dono": {"nome_dono": nome_dono},
        "email_dono": {"email_dono": email_dono},
        "comentarios": []
    }
    mycol.insert_one(produto)
    print("Produto criado com sucesso!")

def read_produto(nome=""):
    mycol = db.produto

    produtos = list(mycol.find())
    if not produtos:
        print("Não existem produtos cadastrados.")
        return

    if not nome:
        mydoc = mycol.find().sort("nome")
        for x in mydoc:
            print ("Nome: ", x["nome"], "|", "Valor: ", x["valor"])
    else:
        mydoc = mycol.find({"nome": nome})
        for x in mydoc:
            printer.pprint(x)

def update_produto(nome):
    mycol = db.produto

    produtos = list(mycol.find())
    if not produtos:
        print("Não existem produtos cadastrados.")
        return

    myquery = {"nome": nome}
    mydoc = mycol.find_one(myquery)
    if not mydoc:
        print("Produto não encontrado!")
        return

    print("Dados atuais:")
    printer.pprint(mydoc)
    print("Digite os novos dados (deixe vazio para manter)")

    while True:
        novo_nome = input("Novo nome: ")
        if mycol.find_one({"nome": novo_nome}):
            print("Produto com esse nome já existe!")
            continue
        else:
            mydoc["nome"] = novo_nome if novo_nome else mydoc["nome"]
            break

    descricao = input("Nova descrição: ")
    mydoc["descricao"] = descricao if descricao else mydoc["descricao"]

    while True:
        valor = input("Novo valor: ")
        if not valor:
            break
        try:
            valor = float(valor)
            break
        except ValueError:
            print("Valor inválido. Digite um número.")
    mydoc["valor"] = float(valor) if valor else mydoc["valor"]

    newvalues = {"$set": mydoc}
    mycol.update_one(myquery, newvalues)
    print("Produto atualizado com sucesso!")

def delete_produto(nome):
    mycol = db.produto

    if not mycol.find_one({"nome": nome}): 
        print("Produto não encontrado.")
        return

    produtos = list(mycol.find())
    if not produtos:
        print("Não existem produtos cadastrados.")
        return

    myquery = {"nome": nome}
    mycol.delete_one(myquery)
    print(f"Produto {nome} deletado!")