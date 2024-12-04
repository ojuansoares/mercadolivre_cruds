from db.connectionneo4j import get_session
import uuid

def create_usuario():
    session = get_session()
    if session:
        try:
            print()
            nome = input("Digite o nome do usuário: ")
            email = input("Digite o email do usuário: ")
            cpf = input("Digite o CPF do usuário: ")
            senha = input("Digite a senha do usuário: ")
            result = session.execute_write(
                lambda tx: tx.run(
                    "CREATE (u:Usuario {id: $id, nome: $nome, email: $email, cpf: $cpf, senha: $senha}) RETURN u",
                    id=str(uuid.uuid4()), nome=nome, email=email, cpf=cpf, senha=senha
                ).single()
            )
            print()
            print(f"Usuário criado com sucesso: {result}")
        except Exception as e:
            print()
            print(f"Erro ao criar usuário: {e}")
        finally:
            session.close()
    else:
        print("Failed to create session")

def read_usuario(nome):
    session = get_session()
    if session:
        try:
            if not nome:
                result = session.execute_read(
                    lambda tx: list(tx.run("MATCH (u:Usuario) RETURN u"))
                )
            else:
                result = session.execute_read(
                    lambda tx: list(tx.run("MATCH (u:Usuario {nome: $nome}) RETURN u", nome=nome))
                )
            print()
            for record in result:
                print(f"Usuário encontrado: {record['u']['nome']}, Email: {record['u']['email']}, CPF: {record['u']['cpf']}")
        except Exception as e:
            print()
            print(f"Erro ao ler usuário: {e}")
        finally:
            session.close()
    else:
        print()
        print("Failed to create session")