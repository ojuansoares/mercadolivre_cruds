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
                print(f"Nome: {usuario['nome']}, Email: {usuario['email']}, CPF: {usuario['cpf']}")
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

def create_vendedor():
    usuarios = list_usuarios()
    if not usuarios:
        print()
        print("Nenhum usuário encontrado.")
        return

    print()
    usuario_cpf = input("Digite o CPF do usuário que deseja tornar vendedor: ")
    selected_usuario = next((u for u in usuarios if u["cpf"] == usuario_cpf), None)

    if not selected_usuario:
        print()
        print("Usuário não encontrado.")
        return

    session = get_session()
    if session:
        try:
            result = session.execute_write(
                lambda tx: tx.run(
                    "MATCH (u:Usuario {id: $id}) "
                    "CREATE (u)-[:VENDEDOR]->(v:Vendedor {id: $id, nome: $nome, email: $email, cpf: $cpf}) "
                    "RETURN v",
                    id=selected_usuario["id"], nome=selected_usuario["nome"], email=selected_usuario["email"], cpf=selected_usuario["cpf"]
                ).single()
            )
            print()
            print(f"Usuário {selected_usuario['nome']} agora é um vendedor: {result}")
        except Exception as e:
            print()
            print(f"Erro ao criar vendedor: {e}")
        finally:
            session.close()
    else:
        print()
        print("Failed to create session")

def read_vendedor(nome_vendedor):
    session = get_session()
    if session:
        try:
            if nome_vendedor:
                query = "MATCH (u:Usuario)-[:VENDEDOR]->(v:Vendedor {nome: $nome}) RETURN u, v"
                parameters = {"nome": nome_vendedor}
            else:
                query = "MATCH (u:Usuario)-[:VENDEDOR]->(v:Vendedor) RETURN u, v"
                parameters = {}

            result = session.execute_read(
                lambda tx: list(tx.run(query, parameters))
            )
            print()
            for record in result:
                vendedor = record["v"]
                print(f"Vendedor: {vendedor['nome']}, Email: {vendedor['email']}, CPF: {vendedor['cpf']}")
        except Exception as e:
            print()
            print(f"Erro ao listar vendedores: {e}")
        finally:
            session.close()
    else:
        print()
        print("Failed to create session")