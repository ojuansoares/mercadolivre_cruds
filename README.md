# 🛒 Projeto Mercado Livre

Este é um projeto de **Loja Online** inspirado no **Mercado Livre**, desenvolvido em Python com conexão ao MongoDB. O projeto tem funcionalidades de gerenciamento de usuários, vendedores e produtos.

## 📚 Funcionalidades

- CRUD de Usuários
- CRUD de Vendedores
- CRUD de Produtos
- Compras, Favoritos e Comentários

---

## 🚀 Tecnologias Utilizadas

- **Python** (Versão 3.10+)
- **Flask** (para criação de API)
- **MongoDB** (banco de dados NoSQL)
- **PyMongo** (conexão Python com MongoDB)

---

## 📋 Pré-requisitos

Antes de começar, você vai precisar ter instalado:

- **Python 3.10+**
- **MongoDB** (instância local ou remota)

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
.venv\Scripts\activate
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configurar o banco de dados MongoDB:**

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:

```
MONGO_URI=mongodb://localhost:27017/nome-do-seu-banco
```

> Substitua `localhost:27017` se estiver usando uma instância remota do MongoDB.

---

## 🏃‍♂️ Como Rodar o Projeto

1. Certifique-se de que o MongoDB esteja rodando.

2. Execute o arquivo principal da aplicação:

```bash
python app.py
```
