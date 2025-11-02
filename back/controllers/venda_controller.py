from back.models.venda import criar_venda, obter_venda_por_id, obter_vendas_por_usuario
from back.models.produto import getProdutos

class VendaController:
    
    def processar_compra(self, usuario_id, itens_carrinho):
        """
        Processa uma compra completa
        
        Args:
            usuario_id: ID do usuário
            itens_carrinho: Lista de itens do carrinho
        
        Returns:
            Dict com resultado da operação
        """
        try:
            if not usuario_id:
                return {"success": False, "message": "ID do usuário é obrigatório"}
            
            if not itens_carrinho or len(itens_carrinho) == 0:
                return {"success": False, "message": "Carrinho vazio"}
            
            produtos_db = getProdutos()
            produtos_dict = {produto[0]: produto for produto in produtos_db}
            
            itens_validados = []
            total_compra = 0.0
            
            for item in itens_carrinho:
                produto_encontrado = None
                for produto in produtos_db:
                    # Assumindo que o ID está disponível no item do carrinho
                    if produto[0] == item.get('produto_id'):  # Ajuste
                        produto_encontrado = produto
                        break
                
                if not produto_encontrado:
                    return {"success": False, "message": f"Produto ID {item.get('produto_id')} não encontrado"}
                
                estoque = produto_encontrado[4]  # Ajuste o índice do estoque
                preco = float(produto_encontrado[2])  # Ajuste o índice do preco
                nome = produto_encontrado[0]  # Ajuste o índice do nome
                
                quantidade = item.get('quantidade', 1)
                
                if estoque < quantidade:
                    return {
                        "success": False, 
                        "message": f"Estoque insuficiente para {nome}. Disponível: {estoque}"
                    }
                
                subtotal = preco * quantidade
                total_compra += subtotal
                
                itens_validados.append({
                    'produto_id': item.get('produto_id'),
                    'quantidade': quantidade,
                    'preco_unitario': preco,
                    'subtotal': subtotal
                })
            
            # Criar venda no banco
            venda_id = criar_venda(usuario_id, total_compra, itens_validados)
            
            if venda_id:
                return {
                    "success": True,
                    "message": "Compra realizada com sucesso!",
                    "venda_id": venda_id,
                    "total": total_compra
                }
            else:
                return {"success": False, "message": "Erro ao processar venda no banco de dados"}
                
        except Exception as e:
            return {"success": False, "message": f"Erro ao processar compra: {str(e)}"}
    
    def obter_historico_compras(self, usuario_id):
        """Obtém o histórico de compras do usuário"""
        try:
            vendas = obter_vendas_por_usuario(usuario_id)
            
            return {
                "success": True,
                "vendas": vendas,
                "total_compras": len(vendas)
            }
            
        except Exception as e:
            return {"success": False, "message": f"Erro ao obter histórico: {str(e)}"}
    
    def obter_detalhes_venda(self, venda_id, usuario_id):
        """Obtém detalhes de uma venda específica"""
        try:
            venda_completa = obter_venda_por_id(venda_id)
            
            if not venda_completa:
                return {"success": False, "message": "Venda não encontrada"}
            
            # Verificar se a venda pertence ao usuário
            if venda_completa['venda']['usuario_id'] != usuario_id:
                return {"success": False, "message": "Acesso não autorizado"}
            
            return {
                "success": True,
                "venda": venda_completa['venda'],
                "itens": venda_completa['itens']
            }
            
        except Exception as e:
            return {"success": False, "message": f"Erro ao obter detalhes da venda: {str(e)}"}