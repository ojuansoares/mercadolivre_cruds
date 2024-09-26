from db.connectionmongo import db
import pprint
from bson.objectid import ObjectId

printer = pprint.PrettyPrinter(indent=2)

def create_vendedor():
    mycol_vendedores = db.vendedor
    mycol_usuarios = db.usuario

    usuarios = list(mycol_usuarios.find())
    if not usuarios:
        print("Não existem usuários cadastrados. Não é possível criar um vendedor.")
        return

    print("Usuários existentes:")
    for idx, usuario in enumerate(usuarios):
        print(f"{idx} - Nome: {usuario['nome']}, Sobrenome: {usuario['sobrenome']}, CPF: {usuario['cpf']}")

    while True:
        try:
            indice = int(input("Digite o índice do usuário para criar o vendedor: "))
            if 0 <= indice < len(usuarios):
                break
            else:
                print("Índice inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    usuario_selecionado = usuarios[indice]

    verifica_vendedor = mycol_vendedores.find_one({"usuario_id": usuario_selecionado["_id"]})
    if verifica_vendedor:
        print("Este usuário já é vendedor.")
        return

    vendedor = {
        "usuario_id": usuario_selecionado["_id"],
        "nome": usuario_selecionado["nome"],
        "sobrenome": usuario_selecionado["sobrenome"],
        "email": usuario_selecionado["email"],
        "vendas": []
    }

    mycol_vendedores.insert_one(vendedor)
    print("Vendedor criado com sucesso!")

def read_vendedor(nome=""):
    mycol = db.vendedor

    vendedores = list(mycol.find())
    if not vendedores:
        print("Não existem vendedores cadastrados.")
        return

    if not nome:
        mydoc = mycol.find().sort("nome")
        for x in mydoc:
            print ("Nome: ", x["nome"], x["sobrenome"], "|", "E-mail: ", x["email"])
    else:
        mydoc = mycol.find({"nome": nome})
        for x in mydoc:
            print ("Nome: ", x["nome"], x["sobrenome"], "|", "E-mail: ", x["email"])


def update_vendedor(nome):
    mycol = db.vendedor
    mycol_produtos = db.produto
    mycol_usuarios = db.usuario

    vendedores = list(mycol.find())
    if not vendedores:
        print("Não existem vendedores cadastrados.")
        return

    myquery = {"nome": nome}
    vendedor = mycol.find_one(myquery)
    if not vendedor:
        print()
        print("Vendedor não encontrado.")
        return

    print()
    print("Dados atuais do vendedor:")
    printer.pprint(vendedor)
    print()
    print("Digite os novos dados (deixe vazio para manter)")
    nome = input("Novo nome: ")
    vendedor["nome"] = nome if nome else vendedor["nome"]
    sobrenome = input("Novo sobrenome: ")
    vendedor["sobrenome"] = sobrenome if sobrenome else vendedor["sobrenome"]

    while True:
        email = input("E-mail: ")
        if mycol.find_one({"email": email}) or mycol_usuarios.find_one({"email": email}):
            print("E-mail já cadastrado!")
            continue
        else:
            vendedor["email"] = email if email else vendedor["email"]
            break

    newvalues = {"$set": {
        "nome": vendedor["nome"],
        "sobrenome": vendedor["sobrenome"],
        "email": vendedor["email"]
    }}
    mycol.update_one({"_id": ObjectId(vendedor["_id"])}, newvalues)

    newvalues_produtos = {"$set": {
        "nome_dono.nome_dono": vendedor["nome"],
        "email_dono.email_dono": vendedor["email"]
    }}
    result = mycol_produtos.update_many(
        {"id_dono.id_dono": ObjectId(vendedor["_id"])},
        newvalues_produtos
    )

    print(f"Vendedor atualizado com sucesso! {result.modified_count} produtos foram atualizados.")

def delete_vendedor(nome):
    mycol = db.vendedor
    mycol_produtos = db.produto
    myquery = {"nome": nome}

    if not mycol.find_one(myquery):
        print("Vendedor não encontrado.")
        return

    vendedores = list(mycol.find())
    if not vendedores:
        print("Não existem vendedores cadastrados.")
        return

    vendedor = mycol.find_one({"usuario_id": mycol.find_one(myquery)["_id"]})
    if vendedor:
        produtos = mycol_produtos.find({"id_dono.id_dono": vendedor["_id"]})
        for produto in produtos:
            mycol_produtos.delete_one({"_id": produto["_id"]})
            print(f"Produto {produto['nome']} deletado!")

    mycol.delete_one(myquery)
    print(f"Vendedor {nome} deletado!")
