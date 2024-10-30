from db.connectioncassandra import session
from uuid import uuid4

def create_usuario():
    session.execute("USE at4;")
    print()

    while True:
        nome = input("Nome: ")
        if nome:
            break
        else:
            print("Nome é um campo obrigatório.")

    while True:
        sobrenome = input("Sobrenome: ")
        if sobrenome:
            break
        else:
            print("Sobrenome é um campo obrigatório.")

    while True:
        cpf = input("CPF: ")
        if not cpf:
            print("CPF é um campo obrigatório.")
            continue
        if not cpf.isdigit():
            print("CPF deve conter apenas números.")
            continue
        if session.execute(f"SELECT cpf FROM usuario WHERE cpf = '{cpf}' ALLOW FILTERING;").one():
            print("CPF já cadastrado!")
            continue
        else:
            break
    
    while True:
        email = input("E-mail: ")
        if not email:
            print("E-mail é um campo obrigatório.")
            continue
        if session.execute(f"SELECT email FROM usuario WHERE email = '{email}' ALLOW FILTERING;").one():
            print("E-mail já cadastrado!")
            continue
        else:
            break

    while True:
        senha = input("Senha: ")
        if senha:
            break
        else:
            print("Senha é um campo obrigatório.")

    key = 1
    enderecos = []
    while key != 'N' and key != 'n':
        rua = input("Rua: ")
        num = input("Num: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        cep = input("CEP: ")
        endereco = {
            "rua": rua, "num": num, "bairro": bairro,
            "cidade": cidade, "estado": estado, "cep": cep
        }
        enderecos.append(endereco)
        key = input("Deseja cadastrar um novo endereço (S/N)? ")
    
    favoritos = []
    compras = []

    session.execute(
        "INSERT INTO usuario (id, nome, sobrenome, cpf, email, senha, endereco, favoritos, compras) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
        (uuid4(), nome, sobrenome, cpf, email, senha, enderecos, favoritos, compras)
    )

    print()
    print("Usuário criado com sucesso!")

def read_usuario(cpf):
    session.execute("USE at4;")

    usuarios = session.execute("SELECT cpf FROM usuario;").all()

    usuario_encontrado = session.execute("SELECT * FROM usuario WHERE cpf = %s ALLOW FILTERING;", (cpf,))

    if not usuarios:
        print()
        print("Não existem usuarios cadastrados.")
        return
    
    if cpf != '':

        if not usuario_encontrado:
            print()
            print("Usuario não encontrado.")
            return
        
        elif usuario_encontrado:
            print("*************************")
            usuario = usuario_encontrado.one()
            print(f"ID: {usuario.id}")
            print(f"Nome: {usuario.nome}")
            print(f"Sobrenome: {usuario.sobrenome}")
            print(f"CPF: {usuario.cpf}")
            print(f"E-mail: {usuario.email}")
            print(f"Senha: {usuario.senha}")
            print("*************************")
            print("Endereços:")
            for endereco in usuario.endereco:
                print(f"  Rua: {endereco['rua']}")
                print(f"  Número: {endereco['num']}")
                print(f"  Bairro: {endereco['bairro']}")
                print(f"  Cidade: {endereco['cidade']}")
                print(f"  Estado: {endereco['estado']}")
                print(f"  CEP: {endereco['cep']}")
                print("*************************")
            print(f"Favoritos:")
            if usuario.favoritos:
                for favorito in usuario.favoritos:
                    print("------------------------")
                    print(f"Produto: {favorito['nome']}")
                    print(f"Descrição: {favorito['descricao']}")
                    print(f"Valor: {favorito['valor']}")
            else:
                print("Nenhum favorito registrado.")
                print("*************************")
            print("*************************")
            print("Compras:")
            if usuario.compras:
                for compra in usuario.compras:
                    print("------------------------")
                    print(f"Produto: {compra['produto']}")
                    print(f"Valor Total: {compra['valortotal']}")
                    print(f"Data da Compra: {compra['datacompra']}")
                    print(f"Quantidade: {compra['quantidade']}")
            else:
                print("Nenhuma compra registrada.")
                print("*************************")
            return
        
    if cpf == '':
        print("*************************")
        usuarios = session.execute("SELECT nome, cpf FROM usuario;")
        for usuario in usuarios:
            print(f"Nome: {usuario.nome} | CPF: {usuario.cpf}")
            print("*************************")
        return

def update_usuario(cpf):
    session.execute("USE at4;")

    usuarios = session.execute("SELECT cpf FROM usuario;").all()

    usuario_encontrado = session.execute("SELECT * FROM usuario WHERE cpf = %s ALLOW FILTERING;", (cpf,))

    if not usuarios:
        print()
        print("Não existem usuarios cadastrados.")
        return
    
    if cpf != '':
        if not usuario_encontrado:
            print()
            print("Usuario não encontrado.")
            return
        if usuario_encontrado:
            print("*************************")
            print("Digite os novos dados (deixe vazio para manter)")

            id_u = usuario_encontrado.one().id

            nome = input("Novo nome: ")
            if nome:
                session.execute("UPDATE usuario SET nome = %s WHERE id = %s;", (nome, id_u))

            sobrenome = input("Novo sobrenome: ")
            if sobrenome:
                session.execute("UPDATE usuario SET sobrenome = %s WHERE id = %s;", (sobrenome, id_u))

            while True:
                novo_cpf = input("Novo CPF: ")
                if novo_cpf:
                    if session.execute(f"SELECT cpf FROM usuario WHERE cpf = '{novo_cpf}' ALLOW FILTERING;").one():
                        print("CPF já cadastrado!")
                        continue
                    else:
                        session.execute("UPDATE usuario SET cpf = %s WHERE id = %s;", (novo_cpf, id_u))
                        break
                if novo_cpf == '':
                    break

            while True:
                email = input("Novo e-mail: ")
                if email:
                    if session.execute(f"SELECT email FROM usuario WHERE email = '{email}' ALLOW FILTERING;").one():
                        print("E-mail já cadastrado!")
                        continue
                    else:
                        session.execute("UPDATE usuario SET email = %s WHERE id = %s;", (email, id_u))
                        break
                if email == '':
                    break

            senha = input("Nova senha: ")
            if senha:
                session.execute("UPDATE usuario SET senha = %s WHERE id = %s;", (senha, id_u))
            
            usuario = usuario_encontrado.one()
            enderecos = usuario.endereco

            if enderecos:
                print("Deseja alterar seu(s) endereço(s)?")
                for i, endereco in enumerate(enderecos):
                    print(f"{i}: {endereco['rua']} | {endereco['num']} | {endereco['cep']}")
                indice = input("Digite o índice do endereço que deseja alterar (ou deixe vazio para não alterar): ")
                if indice.isdigit() and int(indice) < len(enderecos):
                    indice = int(indice)
                    endereco_escolhido = enderecos[indice]
                    print("Digite os novos dados do endereço")

                    rua = input("Nova rua: ")
                    if rua:
                        endereco_escolhido['rua'] = rua

                    num = input("Novo número: ")
                    if num:
                        endereco_escolhido['num'] = num

                    bairro = input("Novo bairro: ")
                    if bairro:
                        endereco_escolhido['bairro'] = bairro

                    cidade = input("Nova cidade: ")
                    if cidade:
                        endereco_escolhido['cidade'] = cidade

                    estado = input("Novo estado: ")
                    if estado:
                        endereco_escolhido['estado'] = estado

                    cep = input("Novo CEP: ")
                    if cep:
                        endereco_escolhido['cep'] = cep

                    enderecos[indice] = endereco_escolhido
                    session.execute(
                        "UPDATE usuario SET endereco = %s WHERE id = %s;",
                        (enderecos, id_u)
                    )
            else:
                print("Não existem endereços cadastrados.")

        print()
        print("Atualização Concluída!")
        return
    else:
        print("Usuario não Encontrado!")
        return