import sqlite3

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


if __name__ == "__main__":
    cria_tabela_produtos()
