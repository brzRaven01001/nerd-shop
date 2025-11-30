import psycopg2

def cria_banco():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres123",
        host="localhost",
        port="5432"
    )
    conn.autocommit = True
    conn.set_client_encoding('UTF8')
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE loja ENCODING 'UTF8' LC_COLLATE='pt_BR.UTF-8' LC_CTYPE='pt_BR.UTF-8' TEMPLATE template0")
    cursor.close()
    conn.close()
    print("Banco 'loja' criado com sucesso!")

def cria_tabela_produtos():
    try:
        conn = psycopg2.connect(
            dbname="loja",
            user="postgres",
            password="postgres123",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                descricao TEXT NOT NULL,
                preco NUMERIC(10, 2) NOT NULL,
                categoria TEXT NOT NULL,
                estoque INTEGER NOT NULL,
                imagem_url TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.set_client_encoding('UTF8')
        cursor.close()
        conn.close()
        print("Tabela 'produtos' criada com sucesso no PostgreSQL!")
    except Exception as e:
        print("Erro ao criar tabela:", e)

def criar_tabela_usuario():
    try:
        conn = psycopg2.connect(
            dbname="loja",
            user="postgres",
            password="postgres123",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.set_client_encoding('UTF8')
        cursor.close()
        conn.close()
        print("Tabela 'usuarios' criada com sucesso no PostgreSQL!")
    except Exception as e:
        print("Erro ao criar tabela:", e)

def criar_tabela_vendas():
    try:
        conn = psycopg2.connect(
            dbname="loja",
            user="postgres",
            password="postgres123",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER REFERENCES usuarios(id),
                total NUMERIC(10, 2) NOT NULL,
                data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) DEFAULT 'concluida',
                forma_pagamento VARCHAR(50),
                status_pagamento VARCHAR(50) DEFAULT 'pendente'
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens_venda (
                id SERIAL PRIMARY KEY,
                venda_id INTEGER REFERENCES vendas(id) ON DELETE CASCADE,
                produto_id INTEGER REFERENCES produtos(id),
                quantidade INTEGER NOT NULL,
                preco_unitario NUMERIC(10, 2) NOT NULL,
                subtotal NUMERIC(10, 2) NOT NULL
            )
        """)
        conn.commit()
        conn.set_client_encoding('UTF8')
        cursor.close()
        conn.close()
        print("Tabelas de vendas criadas com sucesso no PostgreSQL!")
    except Exception as e:
        print("Erro ao criar tabelas de vendas:", e)

def criar_tabela_avaliacoes():
    try:
        conn = psycopg2.connect(
            dbname="loja",
            user="postgres",
            password="postgres123",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS avaliacoes (
                id SERIAL PRIMARY KEY,
                produto_id INTEGER REFERENCES produtos(id) ON DELETE CASCADE,
                nota INTEGER NOT NULL,
                comentario TEXT,
                data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Tabela 'avaliacoes' criada com sucesso!")
    except Exception as e:
        print("Erro ao criar tabela avaliacoes:", e)

def atualizar_tabela_vendas():
    try:
        conn = psycopg2.connect(
            dbname="loja",
            user="postgres",
            password="postgres123",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'vendas' AND column_name = 'forma_pagamento'
        """)
        coluna_existe = cursor.fetchone()
        if not coluna_existe:
            cursor.execute("""
                ALTER TABLE vendas 
                ADD COLUMN forma_pagamento VARCHAR(50),
                ADD COLUMN status_pagamento VARCHAR(50) DEFAULT 'pendente'
            """)
            print("Colunas de pagamento adicionadas à tabela vendas!")
        else:
            print("Colunas de pagamento já existem na tabela vendas!")
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Erro ao atualizar tabela vendas:", e)

def verificar_e_criar_tabelas():
    try:
        cria_banco()
    except Exception as e:
        print(f"Banco já existe ou erro ao criar: {e}, continuando...")
    try:
        cria_tabela_produtos()
    except Exception as e:
        print(f"Tabela produtos já existe ou erro ao criar: {e}, continuando...")
    try:
        criar_tabela_usuario()
    except Exception as e:
        print(f"Tabela usuarios já existe ou erro ao criar: {e}, continuando...")
    try:
        criar_tabela_vendas()
    except Exception as e:
        print(f"Tabelas de vendas já existem ou erro ao criar: {e}, continuando...")
    try:
        criar_tabela_avaliacoes()
    except Exception as e:
        print(f"Tabela avaliacoes já existe ou erro ao criar: {e}, continuando...")
    try:
        atualizar_tabela_vendas()
    except Exception as e:
        print(f"Erro ao atualizar tabela vendas: {e}, continuando...")

def conectar():
    return psycopg2.connect(
        dbname="loja",
        user="postgres",
        password="postgres123",
        host="localhost",
        port="5432"
    )


if __name__ == "__main__":
    print("=== INICIANDO CONFIGURAÇÃO DO BANCO DE DADOS ===")
    verificar_e_criar_tabelas()
    print("=== CONFIGURAÇÃO DO BANCO CONCLUÍDA ===")
