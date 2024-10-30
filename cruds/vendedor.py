from db.connectioncassandra import session
from uuid import uuid4

def create_vendedor():
    session.execute("USE at4;")

    usuarios = session.execute("SELECT * FROM usuario;").all()

    if not usuarios:
        print()
        print("Não existem usuarios cadastrados.")
        return

    print()
    if usuarios:
        for i, usuario in enumerate(usuarios):
            print(f"{i}: Nome: {usuario.nome} | CPF: {usuario.cpf}")
        
        print()
        indice = input("Digite o índice do Usuario que deseja tornar Vendedor: ")
        if indice.isdigit() and int(indice) < len(usuarios):
            indice = int(indice)
        else:
            print()
            print("Índice inválido.")
            return


    usuario = usuarios[indice]

    verificacao_vendedor = session.execute("SELECT usuario_id FROM vendedor WHERE usuario_id = %s ALLOW FILTERING;", (usuario.id,))

    if verificacao_vendedor:
        print("Este usuário já é vendedor.")
        return

    vendas = []

    session.execute(
        "INSERT INTO vendedor (id, usuario_id, nome, sobrenome, email, vendas) VALUES (%s, %s, %s, %s, %s, %s);",
        (uuid4(), usuario.id, usuario.nome, usuario.sobrenome, usuario.email, vendas)
    )
    print()
    print(f"Vendedor '{usuario.nome}' criado com sucesso.")

def read_vendedor(nome=""):
    session.execute("USE at4;")

    vendedores = session.execute("SELECT * FROM vendedor;").all()

    if not vendedores:
        print()
        print("Não existem vendedores cadastrados.")
        return
    
    vendedor_encontrado = session.execute("SELECT * FROM vendedor WHERE nome = %s ALLOW FILTERING;", (nome,))

    if nome == '':
        print("*************************")
        vendedores = session.execute("SELECT nome, email FROM vendedor;")
        for vendedor in vendedores:
            print(f"Nome: {vendedor.nome} | CPF: {vendedor.email}")
            print("*************************")
        return
    elif vendedor_encontrado:
        vendedor_unico = vendedor_encontrado.one()
        print("*************************")
        print(f"ID: {vendedor_unico.id}")
        print(f"ID do Usuário: {vendedor_unico.usuario_id}")
        print(f"Nome: {vendedor_unico.nome}")
        print(f"Sobrenome: {vendedor_unico.sobrenome}")
        print(f"E-mail: {vendedor_unico.email}")
        print("*************************")
        if vendedor_unico.vendas:
            for venda in vendedor_unico.vendas:
                print(f"Comprador: {venda['comprador']}")
                print(f"CPF: {venda['cpf']}")
                print(f"Valor Total da Venda: {venda['valor_total_venda']}")
                print(f"Data da Compra: {venda['data_compra']}")
                print(f"Quantidade: {venda['quantidade']}")
                print("Itens Comprados:")
                for item in venda['compra']:
                    print(f"  Produto: {item['produto']}")
                    print(f"  Valor Total: {item['valor_total']}")
                print("*************************")
        else:
            print("Nenhuma venda registrada.")
        return
    else:
        print()
        print("Vendedor não encontrado.")
        return
