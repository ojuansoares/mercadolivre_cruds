from db.connectionneo4j import check_neo4j_connection
from cruds.usuario import create_usuario, read_usuario
from cruds.vendedor import create_vendedor, read_vendedor
from cruds.produto import create_produto, read_produto
from cruds.compra import create_compra, read_compras
from cruds.favorito import create_favorito, read_favoritos
from cruds.comentario import create_comentario, read_comentarios

def main_menu():
    print("Iniciando conexção com neo4j...")
    check_neo4j_connection()

    print()
    print("Bem-vindo ao Mercado Livre! :)")

    key = 0
    while key != 'S' and key != 's':
        print()
        print("1 - Usuário")
        print("2 - Vendedor")
        print("3 - Produto")
        print("4 - Compras")
        print("5 - Favoritos")
        print("6 - Comentarios")
        key = input("Digite a opção desejada (S para sair): ")

        if key == '1':
            usuario_menu()
        elif key == '2':
            vendedor_menu()
        elif key == '3':
            produto_menu()
        elif key == '4':
            compra_menu()
        elif key == '5':
            menu_favoritos()
        elif key == '6':
            menu_comentarios()

    print()
    print("Foi um prazer... :)")

def usuario_menu():
    sub = 0
    while sub != 'V' and sub != 'v':
        print()
        print("1 - Create Usuário")
        print("2 - Read Usuário")
        sub = input("Digite a opção desejada (V para voltar): ")

        if sub == '1':
            create_usuario()
        elif sub == '2':
            print()
            cpf = input("CPF para pesquisa (deixe em branco para listar todos): ")
            read_usuario(cpf)

def vendedor_menu():
    sub = 0
    while sub != 'V' and sub != 'v':
        print()
        print("1-Create Vendedor")
        print("2-Read Vendedor")
        sub = input("Digite a opção desejada (V para voltar): ")

        if sub == '1':
            create_vendedor()
        elif sub == '2':
            print()
            nome = input("Nome para pesquisa (deixe em branco para listar todos): ")
            read_vendedor(nome)

def produto_menu():
    sub = 0
    while sub != 'V' and sub != 'v':
        print()
        print("1-Create Produto")
        print("2-Read Produto")
        sub = input("Digite a opção desejada (V para voltar): ")

        if sub == '1':
            create_produto()
        elif sub == '2':
            print()
            nome = input("Nome para pesquisa (deixe em branco para listar todos): ")
            read_produto(nome)

def compra_menu():
    sub = 0
    while sub != 'V' and sub != 'v':
        print()
        print("1-Realizar Compra")
        print("2-Listar Compras")
        sub = input("Digite a opção desejada (V para voltar): ")

        if sub == '1':
            create_compra()
        elif sub == '2':
            read_compras()

def menu_favoritos():
    sub = 0
    while sub != 'V' and sub != 'v':
        print()
        print("Opções de Favoritos:")
        print("1. Adicionar Favorito")
        print("2. Listar Favoritos")
        sub = input("Digite a opção desejada (V para voltar): ")
        
        if sub == "1":
            create_favorito()
        elif sub == "2":
            read_favoritos()

def menu_comentarios():
    sub = 0
    while sub != 'V' and sub != 'v':
        print()
        print("Opções de Comentários:")
        print("1. Adicionar Comentário")
        print("2. Listar Comentários")
        sub = input("Digite a opção desejada (V para voltar): ")
        
        if sub == "1":
            create_comentario()
        elif sub == "2":
            read_comentarios()

if __name__ == "__main__":
    main_menu()