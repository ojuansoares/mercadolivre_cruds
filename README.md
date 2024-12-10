# 🛒 Projeto Mercado Livre

Este é um projeto de **Loja Online** inspirado no **Mercado Livre**, desenvolvido em Python com conexão ao **Neo4j**. O projeto tem funcionalidades de gerenciamento de usuários, vendedores, produtos, compras, favoritos e comentários.

## 📚 Funcionalidades

- ✅ USUÁRIO: CREATE, READ  
- ✅ VENDEDOR: CREATE, READ  
- ✅ PRODUTO: CREATE, READ  
- ✅ COMPRA: CREATE, READ  
- ✅ FAVORITO: CREATE, READ  
- ✅ COMENTÁRIO: CREATE, READ  

---

## 🚀 Tecnologias Utilizadas

- **Python** (Versão 3.10+)  
- **Neo4j** (banco de dados de grafos)  
- **neo4j-driver** (conexão Python com Neo4j)  

---

## 📋 Pré-requisitos

Antes de começar, você vai precisar ter instalado:

- **Python 3.10+**  
- **Neo4j** (instância local ou remota)  

### Instalar Python

Você pode baixar a versão mais recente do Python no [site oficial](https://www.python.org/downloads/).

---

## ⚙️ Configuração do Ambiente

Siga os passos abaixo para configurar e rodar o projeto em sua máquina local:

1. **Clone o Repositório:**

```bash
git clone https://github.com/ojuansoares/mercadolivre_cruds/neo4j.git
cd mercadolivre_cruds
```

2. Crie um ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate  # No Windows
source .venv/bin/activate  # No macOS/Linux
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configurar o banco de dados Neo4j:

Crie um arquivo .env na raiz do projeto com as seguintes variáveis de ambiente:

```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=seu-usuario
NEO4J_PASSWORD=sua-senha
```

> Substitua localhost, seu-usuario e sua-senha pelos valores adequados à sua configuração do Neo4j.

---

🏃‍♂️ Como Rodar o Projeto

1. Certifique-se de que o Neo4j esteja rodando.

2. Execute o arquivo principal da aplicação:

```bash
python app.py
```
