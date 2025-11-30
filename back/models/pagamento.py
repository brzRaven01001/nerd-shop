import psycopg2
import time

def get_db_connection():
    """Retorna conexão com o PostgreSQL seguindo seu padrão"""
    return psycopg2.connect(
        dbname="loja",  
        user="postgres",      
        password="postgres123",  
        host="localhost",       
        port="5432"             
    )

def obter_formas_pagamento():
    """Retorna as formas de pagamento disponíveis"""
    return [
        {"id": "cartao_credito", "nome": "Cartão de Crédito", "icone": "💳"},
        {"id": "cartao_debito", "nome": "Cartão de Débito", "icone": "💳"},
        {"id": "pix", "nome": "PIX", "icone": "📱"},
        {"id": "boleto", "nome": "Boleto Bancário", "icone": "📄"},
        {"id": "paypal", "nome": "PayPal", "icone": "🌐"}
    ]

def atualizar_forma_pagamento(venda_id, forma_pagamento):
    """Atualiza a forma de pagamento de uma venda"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE vendas 
            SET forma_pagamento = %s, status_pagamento = 'processando'
            WHERE id = %s
        """, (forma_pagamento, venda_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print("Erro ao atualizar forma de pagamento:", e)
        return False

def simular_processamento_pagamento(venda_id, forma_pagamento):
    """Simula o processamento de um pagamento"""
    try:
        # Simular processamento
        time.sleep(2)  # Simula delay de processamento
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Atualizar status para aprovado
        cursor.execute("""
            UPDATE vendas 
            SET status_pagamento = 'aprovado'
            WHERE id = %s
        """, (venda_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "message": f"Pagamento via {forma_pagamento} processado com sucesso!",
            "venda_id": venda_id
        }
        
    except Exception as e:
        print(f"Erro ao processar pagamento: {e}")
        return {
            "success": False,
            "message": f"Erro ao processar pagamento: {str(e)}"
        }