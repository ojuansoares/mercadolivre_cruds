from db.connectioncassandra import session
from uuid import uuid4
from datetime import datetime


def verificar_existencia():
    session.execute("USE at4;")

    produtos = session.execute("SELECT * FROM produto;").all()

    if not produtos:
        print()
        print("Não existem produtos cadastrados")
        return False
    return True

def listar_usuarios():
    session.execute("USE at4;")

    print()
    usuarios = session.execute("SELECT nome, cpf FROM usuario;")
    for usuario in usuarios:
        print(f"Nome: {usuario.nome} | CPF: {usuario.cpf}")
        print("--------------------------")
    return

def listar_produtos():
    session.execute("USE at4;")

    print()
    produtos = session.execute("SELECT nome, descricao, valor FROM produto;")
    for produto in produtos:
        print(f"Nome: {produto.nome} | Valor: {produto.valor}")
        print("--------------------------")
    return

def listar_compras():
    session.execute("USE at4;")

    compras = session.execute("SELECT * FROM compra;").all()

    if not compras:
        print()
        print("Não existem compras registradas.")
        return False

    print()
    print("Compras realizadas:")
    for compra in compras:
        print("*************************")
        print(f"Compra: {compra.id}")
        print(f"Comprador: {compra.comprador}")
        print(f"CPF: {compra.cpf}")
        print(f"Data da Compra: {compra.data_compra}")
        print(f"Quantidade: {compra.quantidade}")
        print(f"Valor Total da Venda: {compra.valor_total_venda}")
        print("--------------------------")
        print("Produtos:")
        for produto in compra.compra:
            print(f"  Produto: {produto['produto']}, Valor Total: {produto['valor_total']}")
            print("--------------------------")

def listar_compras_resumida():
    session.execute("USE at4;")

    compras = session.execute("SELECT * FROM compra;").all()

    print("Compras realizadas:")
    for index, compra in enumerate(compras):
        print("*************************")
        print(f"Index: {index} | Data da Compra: {compra.data_compra}")
        print(f"ID da Compra: {compra.id}")
        print(f"Comprador: {compra.comprador} | Valor da Venda: {compra.valor_total_venda}")

def remover_compra():
    session.execute("USE at4;")
    compras = session.execute("SELECT * FROM compra;").all()

    if not compras:
        print()
        print("Não existem compras cadastrados")
        return
    
    listar_compras_resumida()
    print()

    while True:
        index = input("Digite o Index da compra que deseja remover: ")
        if index.isdigit() and int(index) < len(compras):
            index = int(index)
        else:
            print("Index inválido.")
            continue

        id_compra = compras[index].id
        compra = session.execute("SELECT * FROM compra WHERE id = %s ALLOW FILTERING;", (id_compra,)).one()
        
        if not compra:
            print("Compra não encontrada.")
            continue
        else:
            break

    session.execute("DELETE FROM compra WHERE id = %s;", (id_compra,))

    print()
    print("Compra removida com sucesso.")



def realizar_compra():
    if not verificar_existencia():
        return

    listar_usuarios()
    while True:
        cpf = input("Digite o CPF do comprador: ")
        comprador = session.execute("SELECT * FROM usuario WHERE cpf = %s ALLOW FILTERING;", (cpf,)).one()
        if not comprador:
            print("Usuário não encontrado.")
            continue
        else:
            break

    listar_produtos()
    while True:
        nome_produto = input("Digite o nome do produto: ")
        produto = session.execute("SELECT * FROM produto WHERE nome = %s ALLOW FILTERING;", (nome_produto,)).one()
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

    valor_total = produto.valor * quantidade
    data_compra = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    compra_id = uuid4()

    # Criar lista de produtos para adicionar à compra
    produtos_compra = [
        {'produto': produto.nome, 
         'valor_total': str(produto.valor)
        }
    ]
    print("Produtos da compra: ", produtos_compra)

    # Inserir a compra em si
    session.execute("""
        INSERT INTO compra (id, comprador, cpf, valor_total_venda, data_compra, quantidade, vendedor, compra)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (compra_id, comprador.nome, comprador.cpf, float(valor_total), data_compra, quantidade, produto.id_dono, produtos_compra))

    print("Compra realizada com sucesso!")



    # Obter a lista de compras atual do usuário
    result_compras = session.execute("SELECT compras FROM usuario WHERE cpf = %s ALLOW FILTERING;", (comprador.cpf,)).one()
    compras_atual = result_compras.compras if result_compras and result_compras.compras else []
    
    # Criar lista de compras para adicionar ao usuário
    compras_usuario = {
        'produto': produto.nome, 
        'valortotal': str(valor_total), 
        'datacompra': data_compra, 
        'quantidade': str(quantidade)
    }

    # Adicionar a nova compra à lista de compras atual
    compras_atual.append(compras_usuario)

    # Atualizar a lista de compras do usuário
    session.execute("""
        UPDATE usuario
        SET compras = %s
        WHERE id = %s;
    """, (compras_atual, comprador.id))
    print("Compra vinculada ao usuário.")


    # Obter a lista de vendas atual do vendedor
    result_vendas = session.execute("SELECT vendas FROM vendedor WHERE id = %s ALLOW FILTERING;", (produto.id_dono,)).one()
    vendas_atual = result_vendas.vendas if result_vendas and result_vendas.vendas else []

    # Criar lista de vendas para adicionar ao vendedor
    vendas_vendedor = {
        'comprador': str(comprador.nome), 
        'cpf': str(comprador.cpf), 
        'valor_total_venda': str(valor_total), 
        'data_compra': str(data_compra), 
        'quantidade': str(quantidade), 
        'produto_nome': str(produto.nome),          # Nome do produto
        'produto_valor': str(produto.valor)          # Valor do produto
    }

    # Adicionar a nova venda à lista de vendas atual
    vendas_atual.append(vendas_vendedor)

    # Atualizar a lista de vendas do vendedor
    session.execute("""
        UPDATE vendedor
        SET vendas = %s
        WHERE id = %s;
    """, (vendas_atual, produto.id_dono))
    print("Venda vinculada ao vendedor.")

if __name__ == "__main__":
    realizar_compra()