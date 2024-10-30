from cruds.usuario import create_usuario, read_usuario, update_usuario
from cruds.vendedor import create_vendedor, read_vendedor
from cruds.produto import create_produto, read_produto
from cruds.compra import realizar_compra, listar_compras, remover_compra
from cruds.favorito import adicionar_favorito, remover_favorito, listar_favoritos
from cruds.comentario import adicionar_comentario, remover_comentario, listar_comentarios
from db.connectioncassandra import check_cassandradb_connection, start_dbs

def main_menu():
    check_cassandradb_connection()

    start_dbs()

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
        print("3 - Update Usuário")
        sub = input("Digite a opção desejada (V para voltar): ")

        if sub == '1':
            create_usuario()
        elif sub == '2':
            print()
            cpf = input("CPF para pesquisa (deixe em branco para listar todos): ")
            read_usuario(cpf)
        elif sub == '3':
            print()
            cpf = input("CPF do usuário a ser atualizado: ")
            update_usuario(cpf)

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
        print("3-Remover Compra")
        sub = input("Digite a opção desejada (V para voltar): ")

        if sub == '1':
            realizar_compra()
        elif sub == '2':
            listar_compras()
        elif sub == '3':
            remover_compra()

def menu_favoritos():
    sub = 0
    while sub != 'V' and sub != 'v':
        print()
        print("Opções de Favoritos:")
        print("1. Adicionar Favorito")
        print("2. Remover Favorito")
        print("3. Listar Favoritos")
        sub = input("Digite a opção desejada (V para voltar): ")
        
        if sub == "1":
            adicionar_favorito()
        elif sub == "2":
            remover_favorito()
        elif sub == "3":
            listar_favoritos()

def menu_comentarios():
    sub = 0
    while sub != 'V' and sub != 'v':
        print()
        print("Opções de Comentários:")
        print("1. Adicionar Comentário")
        print("2. Remover Comentário")
        print("3. Listar Comentários")
        sub = input("Digite a opção desejada (V para voltar): ")
        
        if sub == "1":
            adicionar_comentario()
        elif sub == "2":
            remover_comentario()
        elif sub == "3":
            listar_comentarios()

if __name__ == "__main__":
    main_menu()