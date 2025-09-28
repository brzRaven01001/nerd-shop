import psycopg2

def cria_banco():
    conn = psycopg2.connect(
        dbname="postgres",   
        user="postgres",
        password="Semsenh4?",
        host="localhost",
        port="5432"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE loja")

    cursor.close()
    conn.close()
    print("Banco 'loja' criado com sucesso!")
    
    
def cria_tabela_produtos():
    try:
        conn = psycopg2.connect(
            dbname="loja",  
            user="postgres",      
            password="Semsenh4?",  
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
        cursor.close()
        conn.close()
        print("Tabela 'produtos' criada com sucesso no PostgreSQL!")

    except Exception as e:
        print("Erro ao criar tabela:", e)

if __name__ == "__main__":
    cria_banco()
    cria_tabela_produtos()