from db.connectionneo4j import get_session
import uuid

def list_vendedores():
    session = get_session()
    if session:
        try:
            result = session.execute_read(
                lambda tx: list(tx.run("MATCH (u:Usuario)-[:VENDEDOR]->(v:Vendedor) RETURN u, v"))
            )
            vendedores = []
            print()
            for record in result:
                vendedor = record["v"]
                vendedores.append(vendedor)
                print(f"Nome: {vendedor['nome']}, Email: {vendedor['email']}, CPF: {vendedor['cpf']}")
            return vendedores
        except Exception as e:
            print()
            print(f"Erro ao listar vendedores: {e}")
        finally:
            session.close()
    else:
        print()
        print("Failed to create session")
    return []

def create_produto():
    print()
    nome = input("Digite o nome do produto: ")
    descricao = input("Digite a descrição do produto: ")
    valor = float(input("Digite o valor do produto: "))

    vendedores = list_vendedores()
    if not vendedores:
        print()
        print("Nenhum vendedor encontrado.")
        return

    print()
    vendedor_cpf = input("Digite o CPF do vendedor que deseja associar ao produto: ")
    selected_vendedor = next((v for v in vendedores if v["cpf"] == vendedor_cpf), None)

    if not selected_vendedor:
        print()
        print("Vendedor não encontrado.")
        return

    session = get_session()
    if session:
        try:
            result = session.execute_write(
                lambda tx: tx.run(
                    "MATCH (v:Vendedor {id: $vendedor_id}) "
                    "CREATE (v)-[:VENDE]->(p:Produto {id: $id, nome: $nome, descricao: $descricao, valor: $valor}) "
                    "RETURN p",
                    vendedor_id=selected_vendedor["id"], id=str(uuid.uuid4()), nome=nome, descricao=descricao, valor=valor
                ).single()
            )
            print()
            print(f"Produto criado com sucesso: {result}")
        except Exception as e:
            print()
            print(f"Erro ao criar produto: {e}")
        finally:
            session.close()
    else:
        print()
        print("Failed to create session")

def read_produto(nome_produto):
    session = get_session()
    if session:
        try:
            if nome_produto:
                query = "MATCH (v:Vendedor)-[:VENDE]->(p:Produto {nome: $nome}) RETURN v, p"
                parameters = {"nome": nome_produto}
            else:
                query = "MATCH (v:Vendedor)-[:VENDE]->(p:Produto) RETURN v, p"
                parameters = {}

            result = session.execute_read(
                lambda tx: list(tx.run(query, parameters))
            )
            print()
            for record in result:
                vendedor = record["v"]
                produto = record["p"]
                print(f"Produto: {produto['nome']}, Descrição: {produto['descricao']}, Valor: {produto['valor']}, Vendedor: {vendedor['nome']}")
        except Exception as e:
            print()
            print(f"Erro ao listar produtos: {e}")
        finally:
            session.close()
    else:
        print()
        print("Failed to create session")