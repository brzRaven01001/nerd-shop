import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

def get_connection():
    dsn = "dbname=nerdshop user=postgres password=postgres123 host=localhost port=5432"
    return psycopg2.connect(dsn)
    
def cadastra_usuario(nome, email, senha):
    conn = get_connection()
    cur = conn.cursor()

    senha_hash = generate_password_hash(senha)
    try:
        cur.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", 
                   (nome, email, senha_hash))
        conn.commit()
        return True
    except Exception as e:
        print("Erro ao cadastrar:", e)
        return False
    finally:
        cur.close()
        conn.close()
        
def autentica_usuario(email, senha):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, senha FROM usuarios WHERE email = %s", (email,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()

    if usuario and check_password_hash(usuario[2], senha):
        return {"id": usuario[0], "nome": usuario[1], "email": email}
    return None