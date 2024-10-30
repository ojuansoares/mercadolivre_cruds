from cruds.compra import listar_produtos, verificar_existencia
from db.connectioncassandra import session

def adicionar_comentario():
    if not verificar_existencia():
        return
    
    session.execute("USE at4;")
    
    usuarios = session.execute("SELECT * FROM usuario;").all()

    print()
    if usuarios:
        for i, usuario in enumerate(usuarios):
            print(f"{i}: Nome: {usuario.nome} | CPF: {usuario.cpf}")
        print()
        indice = input("Digite o índice do Usuario que deseja adicionar um Comentário: ")
        if indice.isdigit() and int(indice) < len(usuarios):
            indice = int(indice)
        else:
            print()
            print("Índice inválido.")
            return

    usuario = usuarios[indice]

    print()
    listar_produtos()
    while True:
        produto_nome = input("Nome do produto que deseja Comentar: ")
        produto = session.execute("SELECT * FROM produto WHERE nome = %s ALLOW FILTERING;", (produto_nome,)).one()

        if not produto:
            print()
            print("Produto não encontrado.")
            continue
        
        else:
            break
    
    print()
    while True:
        comentario_texto = input("Digite o comentário: ")
        if not comentario_texto:
            print("Comentário não pode ser vazio.")
            continue
        else:
            break

    comentario = {
        "nome": str(usuario.nome),
        "comentario": str(comentario_texto)
    }

    comentarios = produto.comentarios if produto.comentarios is not None else []
    comentarios.append(comentario)

    session.execute("""
        UPDATE produto
        SET comentarios = %s
        WHERE id = %s
    """, (comentarios, produto.id))
    
    print()
    print("Comentário adicionado com sucesso!")

def remover_comentario():
    print()
    listar_produtos()

    produto_nome = input("Nome do produto que deseja remover um comentário: ")
    produto = session.execute("SELECT * FROM produto WHERE nome = %s ALLOW FILTERING;", (produto_nome,)).one()
    if not produto or not produto.comentarios:
        print()
        print("Produto não encontrado ou não possui comentários.")
        return

    print()
    print("Comentários do produto:")
    for i, comentario in enumerate(produto.comentarios):
        print("------------------------")
        print(f"{i}: Nome: {comentario['nome']}, Comentário: {comentario['comentario']}")

    print()
    indice = input("Digite o índice do comentário que deseja remover: ")

    if indice.isdigit() and int(indice) < len(produto.comentarios):
        indice = int(indice)
        produto.comentarios.pop(indice)
        session.execute("""
            UPDATE produto
            SET comentarios = %s
            WHERE id = %s
        """, (produto.comentarios, produto.id))
        print()
        print("Comentário removido com sucesso!")
    else:
        print()
        print("Índice inválido ou nenhum comentário selecionado. Nenhuma alteração feita.")

def listar_comentarios():
    print()
    listar_produtos()

    produto_nome = input("Nome do produto que deseja listar os comentários: ")
    produto = session.execute("SELECT * FROM produto WHERE nome = %s ALLOW FILTERING;", (produto_nome,)).one()
    if not produto or not produto.comentarios:
        print()
        print("Produto não encontrado ou não possui comentários.")
        return

    print()
    print("Comentários do produto:")
    for comentario in produto.comentarios:
        print("------------------------")
        print(f"Nome: {comentario['nome']}, Comentário: {comentario['comentario']}")