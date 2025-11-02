# -*- coding: utf-8 -*-

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
        
        # Tabela de vendas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER REFERENCES usuarios(id),
                total NUMERIC(10, 2) NOT NULL,
                data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) DEFAULT 'concluida'
            )
        """)
        
        # Tabela de itens da venda
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

def verificar_e_criar_tabelas():
    """Verifica e cria todas as tabelas necessárias"""
    try:
        cria_banco()
    except:
        print("Banco já existe ou erro ao criar, continuando...")
    
    try:
        cria_tabela_produtos()
    except:
        print("Tabela produtos já existe ou erro ao criar, continuando...")
    
    try:
        criar_tabela_usuario()
    except:
        print("Tabela usuarios já existe ou erro ao criar, continuando...")
    
    try:
        criar_tabela_vendas()
    except:
        print("Tabelas de vendas já existem ou erro ao criar, continuando...")

if __name__ == "__main__":
    verificar_e_criar_tabelas()