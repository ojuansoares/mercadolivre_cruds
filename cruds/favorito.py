from db.connection import db
from cruds.compra import listar_usuarios, listar_produtos, verificar_existencia

def adicionar_favorito():
    if not verificar_existencia():
            return

    print()
    listar_usuarios()
    while True:
        usuario_cpf = input("CPF do usuário que deseja adicionar um favorito: ")
        usuario = db.usuario.find_one({"cpf": usuario_cpf})
        if not usuario:
            print("Usuário não encontrado.")
            continue
        else:
            break

    print()
    listar_produtos()
    while True:
        produto_nome = input("Nome do produto que deseja favoritar: ")
        produto = db.produto.find_one({"nome": produto_nome})
        if not produto:
            print("Produto não encontrado.")
            continue
        else:
            break
    
    favorito = {
        "nome": produto["nome"],
        "descricao": produto["descricao"],
        "valor": produto["valor"]
    }

    usuario["favoritos"].append(favorito)
    db.usuario.update_one({"_id": usuario["_id"]}, {"$set": {"favoritos": usuario["favoritos"]}})
    print("Produto adicionado aos favoritos com sucesso!")

def remover_favorito():
    print()
    listar_usuarios()

    usuario_cpf = input("CPF do usuário que deseja remover um favorito: ")
    usuario = db.usuario.find_one({"cpf": usuario_cpf})
    if not usuario or not usuario.get("favoritos"):
        print("Usuário não encontrado ou não possui favoritos.")
        return
    
    print()
    print("Favoritos do usuário:")
    for i, favorito in enumerate(usuario["favoritos"]):
        print(f"{i}: Nome: {favorito['nome']}, Descrição: {favorito['descricao']}, Valor: {favorito['valor']}")
    
    indice = input("Digite o índice do favorito que deseja remover: ")
    
    if indice.isdigit() and int(indice) < len(usuario["favoritos"]):
        indice = int(indice)
        usuario["favoritos"].pop(indice)
        db.usuario.update_one({"_id": usuario["_id"]}, {"$set": {"favoritos": usuario["favoritos"]}})
        print("Favorito removido com sucesso!")
    else:
        print("Índice inválido ou nenhum favorito selecionado. Nenhuma alteração feita.")

def listar_favoritos():
    print()
    listar_usuarios()

    usuario_cpf = input("CPF do usuário que deseja listar os favoritos: ")
    usuario = db.usuario.find_one({"cpf": usuario_cpf})
    if not usuario or not usuario.get("favoritos"):
        print("Usuário não encontrado ou não possui favoritos.")
        return
    
    print()
    print("Favoritos do usuário:")
    for i, favorito in enumerate(usuario["favoritos"]):
        print(f"{i}: Nome: {favorito['nome']}, Descrição: {favorito['descricao']}, Valor: {favorito['valor']}")