# 🛒 Projeto Mercado Livre

Este é um projeto de **Loja Online** inspirado no **Mercado Livre**, desenvolvido em Python com conexão ao Cassandra. O projeto tem funcionalidades de gerenciamento de usuários, vendedores, produtos, compras, favoritos e comentários.

## 📚 Funcionalidades

- ✅ USUARIO: INSERT, READ, UPDATE
- ✅ VENDEDOR: INSERT, READ
- ✅ PRODUTO: INSERT, READ
- ✅ COMPRA: INSERT, READ, DELETE
- ✅ FAVORITO: INSERT, READ, DELETE
- ✅ COMENTARIO: INSERT, READ, DELETE

---

## 🚀 Tecnologias Utilizadas

- **Python** (Versão 3.10+)
- **Flask** (para criação de API)
- **Cassandra** (banco de dados NoSQL)
- **cassandra-driver** (conexão Python com Cassandra)

---

## 📋 Pré-requisitos

Antes de começar, você vai precisar ter instalado:

- **Python 3.10+**
- **Cassandra** (instância local ou remota)

### Instalar Python

Você pode baixar a versão mais recente do Python no [site oficial](https://www.python.org/downloads/).

---

## ⚙️ Configuração do Ambiente

Siga os passos abaixo para configurar e rodar o projeto em sua máquina local:

1. **Clone o Repositório:**

```bash
git clone https://github.com/ojuansoares/mercadolivre_cruds.git
cd mercadolivre_cruds
```

2. **Crie um ambiente virtual:**

```bash
python -m venv .venv
.venv\Scripts\activate  # No Windows
source .venv/bin/activate  # No macOS/Linux
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configurar o banco de dados MongoDB:**

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:

```
BUNDLE_PATH=/caminho/para/secure-connect-bundle.zip
PASSWORD_DB=SuaSenhaProBancoDeDadosCassandra
```

> Substitua /caminho/para/secure-connect-bundle.zip pelo caminho real do seu arquivo de conexão segura.

---

## 🏃‍♂️ Como Rodar o Projeto

1. Certifique-se de que o Cassandra esteja rodando.

2. Execute o arquivo principal da aplicação:

```bash
python app.py
```

## 📝 Notas


### Explicação das mudanças:

1. **Atualização das tecnologias utilizadas**:
   - Removido MongoDB e Redis.
   - Adicionado Cassandra.

2. **Atualização das funcionalidades**:
   - Listadas as funcionalidades específicas de CRUD para cada entidade.

3. **Atualização das instruções de configuração**:
   - Instruções para configurar o Cassandra em vez do MongoDB e Redis.
   - Adicionado exemplo de configuração do arquivo  para o Cassandra.

4. **Remoção de funcionalidades não mais presentes**:
   - Removido o sistema de login e a retirada de dados do MongoDB/Redis.
