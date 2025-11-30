# 🎮 NerdShop

![Python](https://img.shields.io/badge/Python-3.9%252B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3%252B-lightgrey)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16%252B-blueviolet)
![License](https://img.shields.io/badge/License-MIT-green)

## 👥 Integrantes
* **Ana Cláudia Monteiro Misquita**
* **Alan Araújo**
* **Fernanda Figueiredo**
* **Kauan Pedrosa Marques**
* **Murilo Leone Fernandes**

---

## 🛒 Sobre o Projeto

A **NerdShop** é uma loja virtual completa desenvolvida em Flask para gamers que buscam equipamentos e acessórios de qualidade. Oferecemos uma experiência completa de e-commerce, desde PCs e consoles até periféricos e acessórios gamers.

### 🎯 Catálogo de Produtos
* 🖥️ PCs e Workstations Gamer
* 🎮 Consoles (PlayStation, Xbox, Nintendo)
* 🎯 Controles e Joysticks
* ⌨️ Teclados e Mouses Mecânicos
* 🎧 Headsets e Áudio
* 🖱️ Mousepads e Acessórios

---

## 🏗️ Estrutura do Projeto

```text
NERD-SHOP/
├── 📁 back/                       # Backend da aplicação
│   ├── 📁 controllers/           # Controladores das rotas
│   ├── 📁 models/                # Modelos de dados
│   ├── atualizar_banco.py        # Script de atualização do banco
│   └── bd.py                     # Configuração do banco de dados
├── 📁 static/                    # Arquivos estáticos
│   └── 📁 src/                   # CSS da aplicação
│       ├── cadastro_usuario.css  # Estilos do cadastro
│       ├── cadastro.css          # Estilos de cadastro geral
│       ├── carinho.css           # Estilos do carrinho
│       ├── confirmacao.css       # Estilos da confirmação
│       ├── login_usuario.css     # Estilos do login
│       ├── pagamento.css         # Estilos do pagamento
│       ├── pc.css                # Estilos da página de PCs
│       ├── produtos.css          # Estilos dos produtos
│       ├── style.css             # Estilos principais
│       └── venda.css             # Estilos de vendas
├── 📁 templates/                 # Templates HTML
│   ├── buscar.html               # Página de busca
│   ├── cadastro_usuario.html     # Cadastro de usuário
│   ├── cadastro.html             # Cadastro geral
│   ├── carinho.html              # Carrinho de compras
│   ├── confirmacao_compra.html   # Confirmação de compra
│   ├── index.html                # Página inicial
│   ├── login_usuario.html        # Login de usuário
│   ├── pagamento.html            # Página de pagamento
│   ├── pc.html                   # Página de PCs
│   └── produto_detalhe.html      # Detalhes do produto
├── app.py                        # Aplicação principal Flask
└── README.md                     # Documentação
```

---

## 🚀 Tecnologias Utilizadas

### 🔹 Backend
* Python 3.9+
* Flask 2.3+
* PostgreSQL (via psycopg2)

### 🔹 Frontend
* HTML5 com Jinja2
* CSS3 (Arquivos modulares)

### 🔹 Banco de Dados
* PostgreSQL

---

## 📦 Instalação e Configuração

### Pré-requisitos
* Python 3.9 ou superior
* PostgreSQL 16 ou superior
* Git

### 🛠️ Configuração Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/brzRaven01001/nerd-shop.git](https://github.com/brzRaven01001/nerd-shop.git)
   cd nerd-shop
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale as dependências do Flask:**
   ```bash
   pip install flask psycopg2-binary python-dotenv
   ```

4. **Configure o banco de dados PostgreSQL:**
   ```bash
   # Conecte ao PostgreSQL e crie o banco
   sudo -u postgres psql

   CREATE DATABASE nerdshop;
   CREATE USER nerdshop_user WITH PASSWORD 'sua_senha_aqui';
   GRANT ALL PRIVILEGES ON DATABASE nerdshop TO nerdshop_user;
   \q
   ```

5. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto:
   ```bash
   echo "DATABASE_URL=postgresql://nerdshop_user:sua_senha_aqui@localhost:5432/nerdshop" > .env
   echo "SECRET_KEY=sua_chave_secreta_muito_segura_aqui" >> .env
   echo "FLASK_ENV=development" >> .env
   ```

6. **Execute o script de atualização do banco:**
   ```bash
   python back/atualizar_banco.py
   ```

7. **Execute a aplicação:**
   ```bash
   python app.py
   ```

8. **Acesse a aplicação:**
   * Site principal: http://localhost:5000

---

## 📋 Funcionalidades Implementadas

### ✅ Sistema de Autenticação
* `cadastro_usuario.html` - Registro de novos usuários
* `login_usuario.html` - Login de usuários
* Sessões de usuário

### ✅ Catálogo de Produtos
* `index.html` - Página inicial com produtos
* `produto_detalhe.html` - Detalhes do produto
* `pc.html` - Página específica para PCs
* `buscar.html` - Sistema de busca

### ✅ Carrinho de Compras
* `carinho.html` - Gestão do carrinho
* Adicionar/remover produtos

### ✅ Processo de Compra
* `pagamento.html` - Finalização do pagamento
* `confirmacao_compra.html` - Confirmação da compra

### ✅ Integração com PostgreSQL
* Modelos em `back/models/`
* Controladores em `back/controllers/`
* Configuração em `back/bd.py`

---

## 🌐 Rotas da Aplicação

### 🔐 Autenticação
* `GET/POST /cadastro_usuario` - Registro de usuário
* `GET/POST /login_usuario` - Login de usuário
* `GET /logout` - Logout

### 🏪 Loja e Produtos
* `GET /` - Página inicial (index.html)
* `GET /produtos` - Lista de produtos
* `GET /produto/<id>` - Detalhes do produto
* `GET /pc` - Página de PCs
* `GET /buscar` - Busca de produtos

### 🛒 Carrinho e Compra
* `GET /carrinho` - Visualizar carrinho
* `POST /carrinho/adicionar` - Adicionar ao carrinho
* `POST /carrinho/remover` - Remover do carrinho
* `GET /pagamento` - Página de pagamento
* `POST /finalizar_compra` - Finalizar compra
* `GET /confirmacao` - Confirmação de compra

---

## 🗃️ Estrutura de CSS

O projeto utiliza CSS modular organizado em:
* `style.css` - Estilos globais e base
* `produtos.css` - Estilos para listagem de produtos
* `pc.css` - Estilos específicos para página de PCs
* `carinho.css` - Estilos do carrinho de compras
* `pagamento.css` - Estilos do processo de pagamento
* `login_usuario.css` - Estilos do sistema de login
* `cadastro_usuario.css` - Estilos do cadastro

---

## 🔧 Comandos Úteis

### Desenvolvimento
```bash
# Executar em modo desenvolvimento
python app.py

# Ou usando Flask run
export FLASK_APP=app.py
flask run --debug
```

### Banco de Dados
```bash
# Executar atualização do banco
python back/atualizar_banco.py

# Verificar conexão com PostgreSQL
psql -h localhost -U nerdshop_user -d nerdshop
```

---

## 🐛 Solução de Problemas

### Erro de Conexão com PostgreSQL
```bash
# Verificar se o PostgreSQL está rodando
sudo systemctl status postgresql

# Verificar conexão
psql -h localhost -U nerdshop_user -d nerdshop
```

### Erro de Importação
```bash
# Verificar se todas as dependências estão instaladas
pip install flask psycopg2-binary python-dotenv

# Verificar estrutura de pastas
ls -la back/controllers/
ls -la back/models/
```

### Problemas de CSS
```bash
# Verificar se os arquivos CSS estão na pasta correta
ls -la static/src/
```

---

## 📞 Suporte e Contato

* **Repositório:** [https://github.com/brzRaven01001/nerd-shop](https://github.com/brzRaven01001/nerd-shop)
* **Issues:** [GitHub Issues](https://github.com/brzRaven01001/nerd-shop/issues)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

<br>

⭐ **Desenvolvido com paixão pela comunidade gamer!**

![GitHub stars](https://img.shields.io/github/stars/brzRaven01001/nerd-shop.svg?style=social)

---