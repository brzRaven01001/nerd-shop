import sqlite3

def cria_tabela_produtos():
    conn = sqlite3.connect("back/produto.db")  # caminho igual ao usado no bd.py
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
        conn = sqlite3.connect("back/produto.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO produtos (nome, descricao, preco, categoria, estoque, imagem_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, descricao, preco, categoria, estoque, imagem_url))
        conn.commit()
        conn.close()
        return {"message": "Produto inserido com sucesso!"}
    except Exception as e:
        return {"error": str(e)}
