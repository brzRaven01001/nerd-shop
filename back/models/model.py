import sqlite3
import os

caminho_banco = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'produto.db')

def cria_tabela_produtos():
    conn = sqlite3.connect("back/produto.db")  
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            preco REAL NOT NULL,
            categoria TEXT NOT NULL,
            estoque INTEGER NOT NULL,
            imagem_url TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("Tabela 'produtos' criada com sucesso!")


def insereProdutoSQL(nome, descricao, preco, categoria, estoque, imagem_url):
    try:
        preco = float(preco)
        estoque = int(estoque)
        print("Tentando inserir:", nome, descricao, preco, categoria, estoque, imagem_url)
        print("Caminho do banco:", caminho_banco)

        conn = sqlite3.connect(caminho_banco)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO produtos (nome, descricao, preco, categoria, estoque, imagem_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, descricao, preco, categoria, estoque, imagem_url))
        conn.commit()
        conn.close()
        print("Produto inserido com sucesso:", nome)
        return None
    except Exception as e:
        print("Erro ao inserir produto:", e)
        return {"error": str(e)}