from db.connectionneo4j import get_session
import uuid

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

def create_comentario():
    usuarios = list_usuarios()
    if not usuarios:
        print()
        print("Nenhum usuário encontrado.")
        return

    print()
    usuario_cpf = input("Digite o CPF do usuário que deseja adicionar um comentário: ")
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
    produto_nome = input("Digite o Nome do produto que deseja comentar: ")
    selected_produto = next((p for p in produtos if p["nome"] == produto_nome), None)

    if not selected_produto:
        print()
        print("Produto não encontrado.")
        return

    print()
    comentario_texto = input("Digite o comentário: ")

    session = get_session()
    if session:
        try:
            result = session.execute_write(
                lambda tx: tx.run(
                    "MATCH (u:Usuario {id: $usuario_id}), (p:Produto {id: $produto_id}) "
                    "CREATE (u)-[:COMENTOU {id: $comentario_id, texto: $texto}]->(p) "
                    "RETURN p",
                    usuario_id=selected_usuario["id"], produto_id=selected_produto["id"], comentario_id=str(uuid.uuid4()), texto=comentario_texto
                ).single()
            )
            print()
            print(f"Comentário adicionado com sucesso: {result}")
        except Exception as e:
            print()
            print(f"Erro ao adicionar comentário: {e}")
        finally:
            session.close()
    else:
        print()
        print("Failed to create session")

def read_comentarios(produto_id):
    session = get_session()
    if session:
        try:
            result = session.execute_read(
                lambda tx: list(tx.run(
                    "MATCH (u:Usuario)-[c:COMENTOU]->(p:Produto {id: $produto_id}) RETURN u, c",
                    produto_id=produto_id
                ))
            )
            print()
            for record in result:
                usuario = record["u"]
                comentario = record["c"]
                print(f"Comentário: {comentario['texto']}, Usuário: {usuario['nome']}, Email: {usuario['email']}")
        except Exception as e:
            print()
            print(f"Erro ao listar comentários: {e}")
        finally:
            session.close()
    else:
        print()
        print("Failed to create session")