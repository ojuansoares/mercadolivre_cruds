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

def create_compra():
    usuarios = list_usuarios()
    if not usuarios:
        print()
        print("Nenhum usuário encontrado.")
        return

    print()
    usuario_cpf = input("Digite o CPF do usuário que deseja fazer a compra: ")
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
    produto_nome = input("Digite o nome do produto que deseja comprar: ")
    selected_produto = next((p for p in produtos if p["nome"] == produto_nome), None)

    if not selected_produto:
        print()
        print("Produto não encontrado.")
        return

    while True:
        try:
            print()
            quantidade = int(input("Digite a quantidade do produto: "))
            if quantidade >= 1:
                break
            else:
                print()
                print("A quantidade deve ser igual ou maior que 1.")
        except ValueError:
            print()
            print("Por favor, digite um número válido.")

    session = get_session()
    if session:
        try:
            compra_id = str(uuid.uuid4())
            result = session.execute_write(
                lambda tx: tx.run(
                    "MATCH (u:Usuario {id: $usuario_id}), (p:Produto {id: $produto_id}) "
                    "CREATE (u)-[:COMPROU {quantidade: $quantidade}]->(c:Compra {id: $compra_id, quantidade: $quantidade})-[:INCLUI]->(p) "
                    "RETURN c",
                    usuario_id=selected_usuario["id"], produto_id=selected_produto["id"], quantidade=quantidade, compra_id=compra_id
                ).single()
            )
            print()
            print(f"Compra realizada com sucesso: {result}")

            # Relacionar o vendedor com a compra
            session.execute_write(
                lambda tx: tx.run(
                    "MATCH (p:Produto {id: $produto_id})<-[:VENDE]-(v:Vendedor), (c:Compra {id: $compra_id}) "
                    "CREATE (v)-[:VENDEU]->(c)",
                    produto_id=selected_produto["id"], compra_id=compra_id
                )
            )
        except Exception as e:
            print()
            print(f"Erro ao realizar compra: {e}")
        finally:
            session.close()
    else:
        print()
        print("Failed to create session")

def read_compras():
    session = get_session()
    if session:
        try:
            result = session.execute_read(
                lambda tx: list(tx.run(
                    "MATCH (u:Usuario)-[:COMPROU]->(c:Compra)-[:INCLUI]->(p:Produto), (v:Vendedor)-[:VENDEU]->(c) "
                    "RETURN u, c, p, v"
                ))
            )
            print()
            for record in result:
                usuario = record["u"]
                compra = record["c"]
                produto = record["p"]
                vendedor = record["v"]
                print(f"Compra ID: {compra['id']}, Quantidade: {compra['quantidade']}, Produto: {produto['nome']}, Vendedor: {vendedor['nome']}, Usuário: {usuario['nome']}")
        except Exception as e:
            print()
            print(f"Erro ao listar compras: {e}")
        finally:
            session.close()
    else:
        print()
        print("Failed to create session")