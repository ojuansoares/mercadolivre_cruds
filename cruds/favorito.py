from db.connectionneo4j import get_session

def list_usuarios():
    session = get_session()
    if session:
        try:
            result = session.execute_read(
                lambda tx: list(tx.run("MATCH (u:Usuario) RETURN u"))
            )
            usuarios = []
            print()
            for record in result:
                usuario = record["u"]
                usuarios.append(usuario)
                print(f"ID: {usuario['id']}, Nome: {usuario['nome']}, Email: {usuario['email']}, CPF: {usuario['cpf']}")
            return usuarios
        except Exception as e:
            print()
            print(f"Erro ao listar usuários: {e}")
        finally:
            session.close()
    else:
        print()
        print("Failed to create session")
    return []

def list_produtos():
    session = get_session()
    if session:
        try:
            result = session.execute_read(
                lambda tx: list(tx.run("MATCH (p:Produto) RETURN p"))
            )
            produtos = []
            print()
            for record in result:
                produto = record["p"]
                produtos.append(produto)
                print(f"ID: {produto['id']}, Nome: {produto['nome']}, Descrição: {produto['descricao']}, Valor: {produto['valor']}")
            return produtos
        except Exception as e:
            print()
            print(f"Erro ao listar produtos: {e}")
        finally:
            session.close()
    else:
        print()
        print("Failed to create session")
    return []

def create_favorito():
    usuarios = list_usuarios()
    if not usuarios:
        print()
        print("Nenhum usuário encontrado.")
        return
    
    print()
    usuario_cpf = input("Digite o CPF do usuário que deseja adicionar um favorito: ")
    selected_usuario = next((u for u in usuarios if u["cpf"] == usuario_cpf), None)

    if not selected_usuario:
        print()
        print("Usuário não encontrado.")
        return

    produtos = list_produtos()
    if not produtos:
        print()
        print("Nenhum produto encontrado.")
        return

    print()
    produto_nome = input("Digite o Nome do produto que deseja favoritar: ")
    selected_produto = next((p for p in produtos if p["nome"] == produto_nome), None)

    if not selected_produto:
        print()
        print("Produto não encontrado.")
        return

    session = get_session()
    if session:
        try:
            result = session.execute_write(
                lambda tx: tx.run(
                    "MATCH (u:Usuario {id: $usuario_id}), (p:Produto {id: $produto_id}) "
                    "CREATE (u)-[:FAVORITOU]->(p) "
                    "RETURN p",
                    usuario_id=selected_usuario["id"], produto_id=selected_produto["id"]
                ).single()
            )
            print()
            print(f"Produto favoritado com sucesso: {result}")
        except Exception as e:
            print()
            print(f"Erro ao adicionar favorito: {e}")
        finally:
            session.close()
    else:
        print()
        print("Failed to create session")

def read_favoritos(usuario_id):
    session = get_session()
    if session:
        try:
            result = session.execute_read(
                lambda tx: list(tx.run(
                    "MATCH (u:Usuario {id: $usuario_id})-[:FAVORITOU]->(p:Produto) RETURN p",
                    usuario_id=usuario_id
                ))
            )
            print()
            for record in result:
                produto = record["p"]
                print(f"Produto Favoritado: {produto['nome']}, Descrição: {produto['descricao']}, Valor: {produto['valor']}")
        except Exception as e:
            print()
            print(f"Erro ao listar favoritos: {e}")
        finally:
            session.close()
    else:
        print()
        print("Failed to create session")