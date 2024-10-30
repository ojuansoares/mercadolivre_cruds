from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra import OperationTimedOut
from dotenv import load_dotenv
import os

load_dotenv()

bundle_path = os.getenv('BUNDLE_PATH')
password_db = os.getenv('PASSWORD_DB')


cloud_config = {
    'secure_connect_bundle': bundle_path
}

auth_provider = PlainTextAuthProvider(username = 'token', password = password_db)

global cluster
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)

global session
session = cluster.connect()

def check_cassandradb_connection():
    try:
        session.execute("SELECT * FROM system.local")
        print()
        print("Conexão com o banco de dados Cassandra realizada com sucesso!")
        print("####################################")
    except Exception as e:
        print()
        print("Erro ao conectar com o banco de dados Cassandra: ", e)

def start_dbs():
    session.execute("USE at4;")
    try:
        session.execute("DROP TABLE IF EXISTS usuario;", timeout=60)
        print("Tabela 'usuario' deletada com sucesso!")
        session.execute("DROP TABLE IF EXISTS vendedor;", timeout=60)
        print("Tabela 'vendedor' deletada com sucesso!")
        session.execute("DROP TABLE IF EXISTS produto;", timeout=60)
        print("Tabela 'produto' deletada com sucesso!")
        session.execute("DROP TABLE IF EXISTS compra;", timeout=60)
        print("Tabela 'compra' deletada com sucesso!")
        print("---------------------------")
    except OperationTimedOut:
        print("Erro: Tempo limite excedido ao tentar deletar a tabela 'usuario'.")

    table_usuario = """ 
    CREATE TABLE IF NOT EXISTS usuario (
        id UUID PRIMARY KEY, 
        nome TEXT, 
        sobrenome TEXT, 
        cpf TEXT, 
        email TEXT, 
        senha TEXT, 
        endereco LIST<FROZEN<MAP<TEXT, TEXT>>>, 
        compras LIST<FROZEN<MAP<TEXT, TEXT>>>, 
        favoritos LIST<FROZEN<MAP<TEXT, TEXT>>> 
    ); 
    """

    table_vendedor = """
    CREATE TABLE IF NOT EXISTS vendedor (
        id UUID PRIMARY KEY,
        usuario_id UUID,
        nome TEXT,
        sobrenome TEXT,
        email TEXT,
        vendas LIST<FROZEN<MAP<TEXT, TEXT>>>
    );
    """

    table_produto = """
    CREATE TABLE IF NOT EXISTS produto (
        id UUID PRIMARY KEY,
        nome TEXT,
        descricao TEXT,
        valor FLOAT,
        id_dono UUID,
        nome_dono TEXT,
        email_dono TEXT,
        comentarios LIST<FROZEN<MAP<TEXT, TEXT>>>
    );
    """
    table_compra = """
    CREATE TABLE IF NOT EXISTS compra (
        id UUID PRIMARY KEY,
        comprador TEXT,
        cpf TEXT,
        valor_total_venda FLOAT,
        data_compra TIMESTAMP,
        quantidade INT,
        vendedor UUID,
        compra LIST<FROZEN<MAP<TEXT, TEXT>>>
    );
    """

    try:
        session.execute(table_usuario, timeout=60)
        print("Tabela 'usuario' criada com sucesso!")
        session.execute(table_vendedor, timeout=60)
        print("Tabela 'vendedor' criada com sucesso!")
        session.execute(table_produto, timeout=60)
        print("Tabela 'produto' criada com sucesso!")
        session.execute(table_compra, timeout=60)
        print("Tabela 'compra' criada com sucesso!")
    except OperationTimedOut:
        print("Erro: Tempo limite excedido ao tentar criar a tabela 'usuario'.")
