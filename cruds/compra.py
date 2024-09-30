from db.connectionmongo import db
import pprint
from datetime import datetime
from cruds.login import verificar_usuario_logado

printer = pprint.PrettyPrinter(indent=2)

def verificar_existencia():
    usuarios_count = db.usuario.count_documents({})
    produtos_count = db.produto.count_documents({})
    if usuarios_count == 0:
        print("Não existem usuários cadastrados.")
        return False
    if produtos_count == 0:
        print("Não existem produtos cadastrados.")
        return False
    return True

def listar_usuarios():
    usuarios = db.usuario.find()
    print("Usuários existentes:")
    for usuario in usuarios:
        print(f"Nome: {usuario['nome']}, | CPF: {usuario['cpf']}")

def listar_produtos():
    produtos = db.produto.find()
    print("Produtos existentes:")
    for x in produtos:
        print(x["nome"], "|", x["valor"])

def listar_compras():
    compras = db.compra.find()

    if not compras:
        print("Não existem compras realizadas.")
        return

    print()
    print("Compras realizadas:")
    print()
    for compra in compras:
        print(f"Compra: {compra['_id']}")
        print(f"Comprador: {compra['comprador']}")
        print(f"CPF: {compra['cpf']}")
        print(f"Data da Compra: {compra['data_compra']}")
        print(f"Quantidade: {compra['quantidade']}")
        print(f"Valor Total da Venda: {compra['valor_total_venda']}")
        print("Produtos:")
        for produto in compra['compra']:
            print(f"  Produto: {produto['produto']}, Valor Total: {produto['valor_total']}")
        print("----------------------------")

def realizar_compra():
    if not verificar_existencia():
        return

    comprador = db.usuario.find_one({"email": verificar_usuario_logado()})

    listar_produtos()
    while True:
        nome_produto = input("Digite o nome do produto: ")
        produto = db.produto.find_one({"nome": nome_produto})
        if not produto:
            print("Produto não encontrado.")
            continue
        else:
            break

    while True:
        quantidade = int(input("Digite a quantidade do produto (1 ou maior): "))
        if quantidade >= 1:
            break
        else:
            print("Quantidade inválida. Por favor, digite um valor igual ou maior que 1.")

    valor_total = produto['valor'] * quantidade
    data_compra = datetime.now().strftime("%d/%m/%Y")

    compra_usuario = {
        "produto": produto['nome'],
        "valortotal": valor_total,
        "datacompra": data_compra,
        "quantidade": quantidade
    }

    compra_vendedor = {
        "comprador": comprador['nome'],
        "cpf": comprador['cpf'],
        "valor_total_venda": valor_total,
        "data_compra": data_compra,
        "quantidade": quantidade,
        "compra": [
            {
                "produto": produto['nome'],
                "valor_total": produto['valor']
            }
        ]
    }

    compra_listadecompras = {
        "comprador": comprador['nome'],
        "cpf": comprador['cpf'],
        "valor_total_venda": valor_total,
        "data_compra": data_compra,
        "quantidade": quantidade,
        "vendedor": produto['id_dono'],
        "compra": [
            {
                "produto": produto['nome'],
                "valor_total": produto['valor']
            }
        ]
    }

    db.usuario.update_one(
        {"email": verificar_usuario_logado()},
        {"$push": {"compras": compra_usuario}}
    )

    db.vendedor.update_one(
        {"usuario_id": comprador["_id"]},
        {"$push": {"vendas": compra_vendedor}}
    )

    db.compra.insert_one(compra_listadecompras)


    print("Compra realizada com sucesso!")
    printer.pprint(compra_listadecompras)

if __name__ == "__main__":
    realizar_compra()