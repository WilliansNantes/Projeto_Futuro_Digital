🚀 Projeto Futuro Digital


📌 Sobre o Projeto

O Projeto Futuro Digital é uma API REST desenvolvida em Python, projetada para realizar o gerenciamento de informações comerciais relacionadas a clientes, fornecedores, produtos, consumo energético e ordens de venda.

O sistema foi estruturado utilizando Flask e SQLAlchemy, permitindo uma arquitetura modular e escalável.

O projeto utiliza banco de dados remoto hospedado na plataforma Render, garantindo maior profissionalismo, acesso remoto e melhor gerenciamento das informações.

Durante o desenvolvimento foram implementadas diversas validações de dados, garantindo consistência e integridade das informações armazenadas.

🎯 Objetivo do Projeto

O objetivo do sistema é fornecer uma estrutura organizada para controle de dados comerciais, permitindo:

cadastro de clientes e fornecedores

registro de consumo energético

gerenciamento de produtos

controle de vendas

classificação automática de clientes por score

🧠 Principais Funcionalidades
👤 Gestão de Usuários

Cadastro de usuários

Validação de dados

Consulta de registros

Atualização de informações

Exclusão de usuários

👥 Gestão de Pessoas

Cadastro de clientes ou leads

Validação de e-mail e telefone

Cálculo automático de score de cliente

Classificação automática de status

📊 Gestão de Consumo

Registro de consumo energético

Atualização automática de registros (UPSERT)

Associação com cliente

📦 Gestão de Produtos

Cadastro de produtos

Associação com fornecedores

🧾 Gestão de Ordens

Registro de vendas

Associação entre clientes e produtos

Controle de status da ordem

🗄️ Evolução do Banco de Dados
Estrutura Inicial

Durante o início do projeto, o banco de dados foi estruturado com as seguintes tabelas:

fornecedor_empresa

ordem

leads

produtos

status

usuario

Ajustes Realizados

Durante o desenvolvimento, foram realizados ajustes estruturais no banco de dados e na programação para atender melhor às necessidades levantadas pelos stakeholders.

Após as alterações, a estrutura final passou a conter as seguintes tabelas:

consumo

fornecedor_empresa

ordem

pessoas

produtos

status

usuario

Essas mudanças proporcionaram maior organização e aderência às necessidades do cliente final.

📊 Diagrama do Banco de Dados

![Configuração da tabela ordem](img/mermaid-diagram)

📂 Estrutura do Projeto
futuro-digital/
│
├── app.py
│
├── conf/
│   └── database.py
│
├── routes/
│   ├── usuario.py
│   ├── pessoa.py
│   ├── ordem.py
│   └── consumo.py
│
├── funcao/
│   └── _perse_decimal.py
│
├── img/
│   ├── config_ordem_1.png
│   ├── config_ordem_2.png
│   └── config_ordem_3.png
│
├── banco de dados.sql
│
└── README.md
📷 Desenvolvimento do Banco

As imagens abaixo mostram etapas da configuração da tabela ordem no banco de dados durante o desenvolvimento do projeto.
![Configuração da tabela ordem](img/Banco_de_dados_conf.company)

![Configuração da tabela ordem](img/Banco_de_dados_conf.order)

![Configuração da tabela ordem](img/Banco_de_dados_conf.order.02)

![Configuração da tabela ordem](img/Banco_de_dados_conf.order.03)

🔐 Validações Implementadas

O sistema possui diversas validações para garantir integridade dos dados:

Validações de Entrada

campos obrigatórios

formato de e-mail

números inteiros e decimais

datas válidas

Validações de Integridade

verificação de existência de registros relacionados

controle de duplicidade

validação de valores positivos

Regras de Negócio

cálculo automático de score de clientes

classificação automática por status

cálculo de média de consumo

📡 Endpoints da API
Usuários
POST   /usuario/insert
GET    /usuario/all
GET    /usuario/{id}
PUT    /usuario/{id}
DELETE /usuario/{id}
Pessoas
POST   /pessoa/insert
GET    /pessoa/all
GET    /pessoa/{id}
PUT    /pessoa/{id}
DELETE /pessoa/{id}
Ordens
POST   /ordem/insert
GET    /ordem/all
GET    /ordem/{id}
PUT    /ordem/{id}
DELETE /ordem/{id}
Consumo
POST   /consumo/insert
GET    /consumo/all
GET    /consumo/{id}
DELETE /consumo/{id}
⚙️ Tecnologias Utilizadas
Linguagens

Python

SQL

Frameworks

Flask

SQLAlchemy

Banco de Dados

PostgreSQL

Infraestrutura

Banco de dados remoto hospedado no Render

▶️ Instalação e Execução
1️⃣ Clonar o repositório
git clone https://github.com/seu-usuario/futuro-digital.git
2️⃣ Entrar na pasta do projeto
cd futuro-digital
3️⃣ Criar ambiente virtual
python -m venv venv
4️⃣ Ativar ambiente virtual

Windows:

venv\Scripts\activate

Linux/Mac:

source venv/bin/activate
5️⃣ Instalar dependências
pip install flask flask_sqlalchemy psycopg2
6️⃣ Criar banco de dados

Importar o arquivo:

banco de dados.sql

no PostgreSQL.

7️⃣ Executar a aplicação
python app.py

A API estará disponível em:

http://localhost:5000
👨‍💻 Autor

Willians Nantes

🎓 Formação

Automação Industrial

Análise e Desenvolvimento de Sistemas

💻 Experiência com

Python

C#

Java

C++

JavaScript

CSS

APIs REST

Banco de Dados

⭐ Projeto desenvolvido para fins acadêmicos e portfólio profissional.