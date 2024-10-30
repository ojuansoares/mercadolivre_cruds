from db.connectioncassandra import session
from uuid import uuid4

def create_produto():
    session.execute("USE at4;")

    vendedores = session.execute("SELECT * FROM vendedor;").all()

    if not vendedores:
        print()
        print("Não existem vendedores cadastrados. Cadastre um vendedor antes de criar um produto.")
        return

    print()
    while True:
        nome = input("Nome do produto: ")
        if session.execute("SELECT nome FROM produto WHERE nome = %s ALLOW FILTERING;", (nome,)).one():
            print("Produto com esse nome já existe!")
            continue
        elif not nome:
            print("Nome é um campo obrigatório.")
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

    print()
    print("Escolha o dono do produto pelo indice:")
    print("*************************")
    vendedores_escolha = session.execute("SELECT nome, email FROM vendedor;")
    for i, vendedor in enumerate(vendedores_escolha):
        print(f"{i}: Nome: {vendedor.nome} | E-mail: {vendedor.email}")
        print("*************************")
    while True:
        try:
            indice = int(input("Digite o índice do vendedor: "))
            if int(indice) >= 0 and int(indice) < len(vendedores):
                break
            else:
                print("Índice inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")
    
    vendedor = vendedores[indice]

    id_dono = vendedor.id
    nome_dono = vendedor.nome
    email_dono = vendedor.email

    comentarios = []

    session.execute("INSERT INTO produto (id, nome, descricao, valor, id_dono, nome_dono, email_dono, comentarios) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", 
    (uuid4(), nome, descricao, valor, id_dono, nome_dono, email_dono, comentarios))

    print()
    print("Produto criado com sucesso!")

def read_produto(nome=""):
    session.execute("USE at4;")

    produtos = session.execute("SELECT * FROM produto;").all()

    if not produtos:
        print()
        print("Não existem produtos cadastrados.")
        return

    produto_encontrado = session.execute("SELECT * FROM produto WHERE nome = %s ALLOW FILTERING;", (nome,))

    if nome == '':
        print("*************************")
        produtos_achados = session.execute("SELECT nome, descricao, valor FROM produto;")
        for produto in produtos_achados:
            print(f"Nome: {produto.nome} | Descricao: {produto.descricao} | Valor: {produto.valor}")
            print("*************************")
        return
    elif produto_encontrado:
        produto_unico = produto_encontrado.one()
        print("*************************")
        print(f"ID: {produto_unico.id}")
        print(f"Nome: {produto_unico.nome}")
        print(f"Descricao: {produto_unico.descricao}")
        print(f"Valor: {produto_unico.valor}")
        print("*************************")
        print(f"Comentarios:")
        if produto_unico.comentarios is None or produto_unico.comentarios == []:
            print("Nenhum comentario.")
        else:
            for comentario in produto_unico.comentarios:
                print("*************************")
                print(f"Usuario: {comentario['nome']} | Comentario: {comentario['comentario']}")
        print("*************************")
    else:
        print()
        print("Produto não encontrado.")