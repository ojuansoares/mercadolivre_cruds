from db.connectionmongo import db
import pprint

printer = pprint.PrettyPrinter(indent=2)

def get_user_by_email(email):
    mycol = db.usuario
    if mycol.find_one({"email": email}):
        return mycol.find_one({"email": email})
    else:
        return False

def create_usuario():
    mycol = db.usuario
    mycol_vendedores = db.vendedor
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
        if mycol.find_one({"cpf": cpf}):
            print("CPF já cadastrado!")
            continue
        else:
            break
    
    while True:
        email = input("E-mail: ")
        if mycol.find_one({"email": email}) or mycol_vendedores.find_one({"email": email}):
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
    end = []
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
        end.append(endereco)
        key = input("Deseja cadastrar um novo endereço (S/N)? ")
    
    usuario = { 
        "nome": nome, "sobrenome": sobrenome, "cpf": cpf, 
        "email": email, "senha": senha, "end": end, 
        "compras": [], "favoritos": [] 
    }
    mycol.insert_one(usuario)
    print("Usuário criado com sucesso!")

def read_usuario(cpf):
    mycol = db.usuario

    myquery = {"cpf": cpf}
    mydoc = mycol.find_one(myquery)

    usuarios = list(mycol.find())
    if not usuarios:
        print("Não existem usuarios cadastrados.")
        return

    if not mydoc:
        mydoc = mycol.find()
        for x in mydoc:
            print ("Nome: ", x["nome"], x["sobrenome"], "|", "E-mail: ", x["email"])
    else:
        mydoc = mycol.find_one({"cpf": cpf})
        if mydoc: 
            printer.pprint(mydoc) 
        else:
            print("Usuario não encontrado")

def update_usuario(cpf):
    from cruds.login import logout
    mycol = db.usuario

    usuarios = list(mycol.find())
    if not usuarios:
        print("Não existem usuarios cadastrados.")
        return

    myquery = {"cpf": cpf}
    mydoc = mycol.find_one(myquery)
    if not mydoc:
        print()
        print("Usuário não encontrado!")
        return
    else:
        print()
        print("Dados atuais do usuário:")
        printer.pprint(mydoc)
        print()
        print("Digite os novos dados (deixe vazio para manter)")

        novo_nome = input("Novo nome: ")
        mydoc["nome"] = novo_nome if novo_nome else mydoc["nome"]
        sobrenome = input("Novo sobrenome: ")
        mydoc["sobrenome"] = sobrenome if sobrenome else mydoc["sobrenome"]

        while True:
            Acpf = input("Novo CPF: ")
            if mycol.find_one({"cpf": Acpf}):
                print("CPF já cadastrado!")
                continue
            else:
                mydoc["cpf"] = Acpf if Acpf else mydoc["cpf"]
                break

        while True:    
            email = input("Novo e-mail: ")
            if mycol.find_one({"email": email}):
                print("E-mail já cadastrado!")
                continue
            else:
                mydoc["email"] = email if email else mydoc["email"]
                break

        senha = input("Nova senha: ")
        mydoc["senha"] = senha if senha else mydoc["senha"]

        if "end" in mydoc and mydoc["end"]:
            print("Deseja alterar seu(s) endereço(s)?")
            for i, endereco in enumerate(mydoc["end"]):
                print(f"{i}: {endereco}")
            
            indice = input("Digite o índice do endereço que deseja alterar (ou deixe vazio para não alterar): ")
            
            if indice.isdigit() and int(indice) < len(mydoc["end"]):
                indice = int(indice)
                print("Digite os novos dados do endereço (deixe vazio para manter)")
                rua = input("Nova rua: ")
                mydoc["end"][indice]["rua"] = rua if rua else mydoc["end"][indice]["rua"]
                num = input("Novo número: ")
                mydoc["end"][indice]["num"] = num if num else mydoc["end"][indice]["num"]
                bairro = input("Novo bairro: ")
                mydoc["end"][indice]["bairro"] = bairro if bairro else mydoc["end"][indice]["bairro"]
                cidade = input("Nova cidade: ")
                mydoc["end"][indice]["cidade"] = cidade if cidade else mydoc["end"][indice]["cidade"]
                estado = input("Novo estado: ")
                mydoc["end"][indice]["estado"] = estado if estado else mydoc["end"][indice]["estado"]
                cep = input("Novo CEP: ")
                mydoc["end"][indice]["cep"] = cep if cep else mydoc["end"][indice]["cep"]
            else:
                print("Índice inválido ou nenhum endereço selecionado. Nenhuma alteração feita nos endereços.")

    newvalues = { "$set": mydoc }
    mycol.update_one(myquery, newvalues)
    print("Usuário atualizado com sucesso!")
    logout()
    

def delete_usuario(cpf):
    from cruds.login import logout
    mycol = db.usuario

    if not cpf:
        print("CPF não informado.")
        return
    
    if not mycol.find_one({"cpf": cpf}):
        print("Usuário não encontrado.")
        return
    
    usuarios = list(mycol.find())
    if not usuarios:
        print("Não existem usuarios cadastrados.")
        return

    mycol_vendedores = db.vendedor
    mycol_produtos = db.produto
    myquery = {"cpf": cpf}

    vendedor = mycol_vendedores.find_one({"usuario_id": mycol.find_one(myquery)["_id"]})
    if vendedor:
        produtos = mycol_produtos.find({"id_dono.id_dono": vendedor["_id"]})
        for produto in produtos:
            mycol_produtos.delete_one({"_id": produto["_id"]})
            print(f"Produto {produto['nome']} deletado!")

    vendedor = mycol_vendedores.find_one({"usuario_id": mycol.find_one(myquery)["_id"]})
    if vendedor:
        mycol_vendedores.delete_one({"usuario_id": vendedor["usuario_id"]})
        print(f"Vendedor {vendedor['nome']} deletado!")

    mycol.delete_one(myquery)

    print(f"Usuário {cpf} deletado!")
    logout()
