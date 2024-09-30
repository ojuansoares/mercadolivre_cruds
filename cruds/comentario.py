from db.connectionmongo import db
from cruds.compra import listar_produtos, verificar_existencia
from cruds.login import verificar_usuario_logado

def adicionar_comentario():
    if not verificar_existencia():
        return

    usuario = db.usuario.find_one({"email": verificar_usuario_logado()})

    print()
    listar_produtos()
    while True:
        produto_nome = input("Nome do produto que deseja comentar: ")
        produto = db.produto.find_one({"nome": produto_nome})
        if not produto:
            print("Produto não encontrado.")
            continue
        else:
            break

    while True:
        comentario_texto = input("Digite o comentário: ")
        if not comentario_texto:
            print("Comentário não pode ser vazio.")
            continue
        else:
            break

    comentario = {
        "nome": usuario["nome"],
        "comentario": comentario_texto
    }

    produto["comentarios"].append(comentario)
    db.produto.update_one({"_id": produto["_id"]}, {"$set": {"comentarios": produto["comentarios"]}})
    print("Comentário adicionado com sucesso!")

def remover_comentario():
    print()
    listar_produtos()

    produto_nome = input("Nome do produto que deseja remover um comentário: ")
    produto = db.produto.find_one({"nome": produto_nome})
    if not produto or not produto.get("comentarios"):
        print("Produto não encontrado ou não possui comentários.")
        return

    print()
    print("Comentários do produto:")
    for i, comentario in enumerate(produto["comentarios"]):
        print(f"{i}: Nome: {comentario['nome']}, Comentário: {comentario['comentario']}")

    indice = input("Digite o índice do comentário que deseja remover: ")

    if indice.isdigit() and int(indice) < len(produto["comentarios"]):
        indice = int(indice)
        produto["comentarios"].pop(indice)
        db.produto.update_one({"_id": produto["_id"]}, {"$set": {"comentarios": produto["comentarios"]}})
        print("Comentário removido com sucesso!")
    else:
        print("Índice inválido ou nenhum comentário selecionado. Nenhuma alteração feita.")

def listar_comentarios():
    print()
    listar_produtos()

    produto_nome = input("Nome do produto que deseja listar os comentários: ")
    produto = db.produto.find_one({"nome": produto_nome})
    if not produto or not produto.get("comentarios"):
        print("Produto não encontrado ou não possui comentários.")
        return

    print()
    print("Comentários do produto:")
    for i, comentario in enumerate(produto["comentarios"]):
        print(f"{i}: Nome: {comentario['nome']}, Comentário: {comentario['comentario']}")