from cruds.compra import listar_produtos, verificar_existencia
from db.connectioncassandra import session

def adicionar_favorito():
    if not verificar_existencia():
            return
    
    usuarios = session.execute("SELECT * FROM usuario;").all()

    print()
    if usuarios:
        for i, usuario in enumerate(usuarios):
            print(f"{i}: Nome: {usuario.nome} | CPF: {usuario.cpf}")
        print()
        indice = input("Digite o índice do Usuario que deseja adicionar um Favorito: ")
        if indice.isdigit() and int(indice) < len(usuarios):
            indice = int(indice)
        else:
            print()
            print("Índice inválido.")
            return

    usuario = usuarios[indice]
    usuario_id = usuario.id

    listar_produtos()
    while True:
        produto_nome = input("Nome do produto que deseja favoritar: ")
        produto = session.execute("SELECT * FROM produto WHERE nome = %s ALLOW FILTERING;", (produto_nome,)).one()
        if usuario.favoritos:
            for favorito in usuario.favoritos:
                if favorito["nome"] == produto_nome:
                    print()
                    print("Produto já favoritado.")
                    return
        if not produto:
            print("Produto não encontrado.")
            continue
        
        else:
            break
    
    favorito = {
        "nome": produto.nome,
        "descricao": produto.descricao,
        "valor": str(produto.valor)
    }

    usuario_favorito = usuario.favoritos if usuario.favoritos is not None else []
    usuario_favorito.append(favorito)

    session.execute("""
        UPDATE usuario
        SET favoritos = %s
        WHERE id = %s
    """, (usuario_favorito, usuario_id))

    print("Produto adicionado aos favoritos com sucesso!")

def remover_favorito():
    print()
    session.execute("USE at4;")

    usuarios = session.execute("SELECT * FROM usuario;").all()

    if not usuarios:
        print()
        print("Não existem usuários cadastrados.")
        return
    
    usuarios = session.execute("SELECT nome, cpf FROM usuario;")
    for usuario in usuarios:
        print(f"Nome: {usuario.nome} | CPF: {usuario.cpf}")
        print("*************************")
    
    print()
    cpf = input("Digite o CPF do usuário que deseja remover um favorito: ")
    if cpf:
        usuario = session.execute("SELECT * FROM usuario WHERE cpf = %s ALLOW FILTERING;", (cpf,)).one()
        if not usuario:
            print("Usuário não encontrado.")
            return
        else:
            print()
            print("Favoritos do usuário:")
            if usuario.favoritos:
                for i, favorito in enumerate(usuario.favoritos):
                    print("------------------------")
                    print(f"{i}: Nome: {favorito['nome']}, Descrição: {favorito['descricao']}, Valor: {favorito['valor']}")
                
                print()
                indice = input("Digite o índice do favorito que deseja remover: ")
                
                if indice.isdigit() and int(indice) < len(usuario.favoritos):
                    indice = int(indice)
                    usuario.favoritos.pop(indice)
                    session.execute("""
                        UPDATE usuario
                        SET favoritos = %s
                        WHERE id = %s
                    """, (usuario.favoritos, usuario.id))
                    print()
                    print("Favorito removido com sucesso!")
                else:
                    print()
                    print("Índice inválido ou nenhum favorito selecionado. Nenhuma alteração feita.")
            else:
                print()
                print("Nenhum favorito registrado.")

def listar_favoritos():
    print()
    session.execute("USE at4;")

    usuarios = session.execute("SELECT * FROM usuario;").all()

    if not usuarios:
        print()
        print("Não existem usuários cadastrados.")
        return
    
    usuarios = session.execute("SELECT nome, cpf FROM usuario;")
    for usuario in usuarios:
        print(f"Nome: {usuario.nome} | CPF: {usuario.cpf}")
        print("*************************")
    
    cpf = input("Digite o CPF do usuário que deseja ver os favoritos: ")
    if cpf:
        usuario = session.execute("SELECT * FROM usuario WHERE cpf = %s ALLOW FILTERING;", (cpf,)).one()
        if not usuario:
            print("Usuário não encontrado.")
            return
        else:
            print()
            print(f"Favoritos:")
            if usuario.favoritos:
                for favorito in usuario.favoritos:
                    print("------------------------")
                    print(f"Produto: {favorito['nome']}")
                    print(f"Descrição: {favorito['descricao']}")
                    print(f"Valor: {favorito['valor']}")
            else:
                print("------------------------")
                print("Nenhum favorito registrado.")