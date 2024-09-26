from cruds.usuario import create_usuario, read_usuario, update_usuario, delete_usuario
from cruds.vendedor import create_vendedor, read_vendedor, update_vendedor, delete_vendedor
from cruds.produto import create_produto, read_produto, update_produto, delete_produto
from cruds.compra import realizar_compra, listar_compras
from cruds.favorito import adicionar_favorito, remover_favorito, listar_favoritos
from cruds.comentario import adicionar_comentario, remover_comentario, listar_comentarios
from cruds.login import login, verificar_e_expirar_login, verificar_usuario_logado, logout

def main_menu():
    key = 0
    while key != 'S' and key != 's':

        while not verificar_e_expirar_login():
            print("Faça login para continuar.")
            login_menu()
            
            if verificar_usuario_logado():
                continue
            if not verificar_usuario_logado():
                return

        print()
        print("1 - Usuário")
        print("2 - Vendedor")
        print("3 - Produto")
        print("4 - Compras")
        print("5 - Favoritos")
        print("6 - Comentarios")
        print("7 - Verificar Usuário Logado")
        print("8 - Fazer Logout")
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
        elif key == '7':
            print(verificar_usuario_logado())
        elif key == '8':
            logout()
            continue

    print("Foi um prazer... :)")

def login_menu():
    sub = 0
    while sub != 'S' and sub != 's':
        print()
        print("1 - Fazer Login")
        print("2 - Cadastrar Usuário")
        sub = input("Digite a opção desejada (S para Sair): ")

        if sub == '1':
            email = input("E-mail: ")
            senha = input("Senha: ")
            login(email, senha)
        elif sub == '2':
            create_usuario()

        if verificar_usuario_logado():
            return
        
def usuario_menu():
    sub = 0
    while sub != 'V' and sub != 'v':
        print()
        print("1 - Create Usuário")
        print("2 - Read Usuário")
        print("3 - Update Usuário")
        print("4 - Delete Usuário")
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
        elif sub == '4':
            print()
            cpf = input("CPF do usuário a ser deletado: ")
            delete_usuario(cpf)

def vendedor_menu():
    sub = 0
    while sub != 'V' and sub != 'v':
        print()
        print("1-Create Vendedor")
        print("2-Read Vendedor")
        print("3-Update Vendedor")
        print("4-Delete Vendedor")
        sub = input("Digite a opção desejada (V para voltar): ")

        if sub == '1':
            create_vendedor()
        elif sub == '2':
            print()
            nome = input("Nome para pesquisa (deixe em branco para listar todos): ")
            read_vendedor(nome)
        elif sub == '3':
            print()
            nome = input("Nome do vendedor a ser atualizado: ")
            update_vendedor(nome)
        elif sub == '4':
            print()
            cpf = input("CPF do vendedor a ser deletado: ")
            delete_vendedor(cpf)

def produto_menu():
    sub = 0
    while sub != 'V' and sub != 'v':
        print()
        print("1-Create Produto")
        print("2-Read Produto")
        print("3-Update Produto")
        print("4-Delete Produto")
        sub = input("Digite a opção desejada (V para voltar): ")

        if sub == '1':
            create_produto()
        elif sub == '2':
            print()
            nome = input("Nome para pesquisa (deixe em branco para listar todos): ")
            read_produto(nome)
        elif sub == '3':
            print()
            nome = input("Nome do produto a ser atualizado: ")
            update_produto(nome)
        elif sub == '4':
            print()
            nome = input("Nome do produto a ser deletado: ")
            delete_produto(nome)

def compra_menu():
    sub = 0
    while sub != 'V' and sub != 'v':
        print()
        print("1-Realizar Compra")
        print("2-Listar Compras")
        sub = input("Digite a opção desejada (V para voltar): ")

        if sub == '1':
            realizar_compra()
        elif sub == '2':
            listar_compras()

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