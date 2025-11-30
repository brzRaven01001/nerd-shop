import os
import psycopg2

caminho_banco = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'produto.db')


def insereProdutoSQL(nome, descricao, preco, categoria, estoque, imagem_url):
    try:
        preco = float(preco)
        estoque = int(estoque)
       
        conn = psycopg2.connect(
            dbname="loja",  
            user="postgres",      
            password="postgres123",  
            host="localhost",       
            port="5432"             
        )
        cursor = conn.cursor()
        cursor.execute("""
             INSERT INTO produtos (nome, descricao, preco, categoria, estoque, imagem_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, descricao, preco, categoria, estoque, imagem_url))
        
        
        conn.commit()
        conn.close()
        print("Produto inserido com sucesso:", nome)
        return None
    except Exception as e:
        print("Erro ao inserir produto:", e)
        return {"error": str(e)}
    

def getProdutos():
    try:
        conn = psycopg2.connect(
            dbname="loja",  
            user="postgres",      
            password="postgres123",  
            host="localhost",       
            port="5432"             
        )
        cur = conn.cursor()
        cur.execute("SELECT nome, descricao, preco, categoria, estoque, imagem_url, id FROM produtos;")
    
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        
        return resultados

    except Exception as e:
        print("Erro ao buscar produtos:", e)
        return []
    
def buscarProdutosSQL(termo):
    try:
        conn = psycopg2.connect(
            dbname="loja",
            user="postgres",
            password="postgres123",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        
        cur.execute("""
            SELECT nome, descricao, preco, categoria, estoque, imagem_url, id 
            FROM produtos
            WHERE LOWER(nome) LIKE %s OR LOWER(categoria) LIKE %s OR LOWER(descricao) LIKE %s;
        """, (f"%{termo.lower()}%", f"%{termo.lower()}%",f"%{termo.lower()}%" ))

        resultados = cur.fetchall()

        cur.close()
        conn.close()

        return resultados

    except Exception as e:
        print("Erro ao buscar produtos:", e)
        return []