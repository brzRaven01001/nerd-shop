import os
import psycopg2

def get_db_connection():
    """Retorna conexão com o PostgreSQL seguindo seu padrão"""
    return psycopg2.connect(
        dbname="loja",  
        user="postgres",      
        password="postgres123",  
        host="localhost",       
        port="5432"             
    )

def criar_venda(usuario_id, total, itens):
    """
    Cria uma nova venda no banco de dados
    
    Args:
        usuario_id: ID do usuário
        total: Valor total da venda
        itens: Lista de itens [{'produto_id': x, 'quantidade': y, 'preco_unitario': z}]
    
    Returns:
        ID da venda criada ou None em caso de erro
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Inserir venda
        cursor.execute("""
            INSERT INTO vendas (usuario_id, total, status)
            VALUES (%s, %s, 'concluida') RETURNING id
        """, (usuario_id, total))
        venda_id = cursor.fetchone()[0]
        
        # Inserir itens da venda
        for item in itens:
            subtotal = item['preco_unitario'] * item['quantidade']
            cursor.execute("""
                INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """, (venda_id, item['produto_id'], item['quantidade'], item['preco_unitario'], subtotal))
            
            # Atualizar estoque
            cursor.execute("""
                UPDATE produtos 
                SET estoque = estoque - %s 
                WHERE id = %s
            """, (item['quantidade'], item['produto_id']))
        
        conn.commit()
        conn.close()
        print("Venda criada com sucesso, ID:", venda_id)
        return venda_id
        
    except Exception as e:
        print("Erro ao criar venda:", e)
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return None

def obter_venda_por_id(venda_id):
    """Obtém uma venda específica por ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Buscar dados da venda
        cursor.execute("""
            SELECT v.*, u.nome as usuario_nome
            FROM vendas v
            LEFT JOIN usuarios u ON v.usuario_id = u.id
            WHERE v.id = %s
        """, (venda_id,))
        venda = cursor.fetchone()
        
        if venda:
            # Buscar itens da venda
            cursor.execute("""
                SELECT iv.*, p.nome as produto_nome, p.imagem_url
                FROM itens_venda iv
                JOIN produtos p ON iv.produto_id = p.id
                WHERE iv.venda_id = %s
            """, (venda_id,))
            itens = cursor.fetchall()
            
            conn.close()
            
            return {
                'venda': {
                    'id': venda[0],
                    'usuario_id': venda[1],
                    'total': float(venda[2]),
                    'data_venda': venda[3],
                    'status': venda[4],
                    'usuario_nome': venda[5]
                },
                'itens': [
                    {
                        'id': item[0],
                        'venda_id': item[1],
                        'produto_id': item[2],
                        'quantidade': item[3],
                        'preco_unitario': float(item[4]),
                        'subtotal': float(item[5]),
                        'produto_nome': item[6],
                        'imagem_url': item[7]
                    } for item in itens
                ]
            }
        
        conn.close()
        return None
        
    except Exception as e:
        print("Erro ao obter venda:", e)
        if 'conn' in locals():
            conn.close()
        return None

def obter_vendas_por_usuario(usuario_id):
    """Obtém todas as vendas de um usuário"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT v.*, 
                   (SELECT COUNT(*) FROM itens_venda iv WHERE iv.venda_id = v.id) as total_itens
            FROM vendas v
            WHERE v.usuario_id = %s
            ORDER BY v.data_venda DESC
        """, (usuario_id,))
        vendas = cursor.fetchall()
        
        conn.close()
        
        return [
            {
                'id': venda[0],
                'usuario_id': venda[1],
                'total': float(venda[2]),
                'data_venda': venda[3],
                'status': venda[4],
                'total_itens': venda[5]
            } for venda in vendas
        ]
        
    except Exception as e:
        print("Erro ao obter vendas do usuário:", e)
        if 'conn' in locals():
            conn.close()
        return []