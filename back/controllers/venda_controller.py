from back.models.venda import criar_venda, obter_venda_por_id, obter_vendas_por_usuario, executar_venda
from back.models.produto import getProdutos
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify


class VendaController:
        
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
        
    def processar_compra(self, usuario_id, itens_compra):
        """Processa a compra com os itens do carrinho"""
        try:
            if not usuario_id:
                return {"success": False, "message": "ID do usuário é obrigatório"}
            
            if not itens_compra:
                return {"success": False, "message": "Carrinho vazio"}
            
            total = 0
            for item in itens_compra:
                total += item['quantidade'] * item['preco_unitario']
            
            # Cria a venda no banco
            venda_id = criar_venda(usuario_id, total, itens_compra)
            
            if venda_id:
                return {"success": True, "venda_id": venda_id}
            else:
                return {"success": False, "message": "Erro ao criar venda no banco"}
        
        except Exception as e:
            return {"success": False, "message": f"Erro ao processar compra: {str(e)}"}
        
            
def executar_venda_controller():
        """Finaliza a venda usando os itens do carrinho"""
        if request.method == "POST":
        
            carrinho = session.get('carrinho', [])
            if not carrinho:
                return jsonify({"success": False, "message": "Carrinho vazio."}), 400

        
            usuario = session.get('usuario')
            if not usuario:
                return jsonify({"success": False, "message": "Usuário não logado."}), 401

            usuario_id = usuario['id'] 

            itens_compra = []
            for item in carrinho:
                itens_compra.append({
                    'produto_id': item['produto_id'],
                    'quantidade': item['quantidade'],
                    'preco_unitario': item['preco']
                })

            venda_controller = VendaController()
            resultado = venda_controller.processar_compra(usuario_id, itens_compra)

            if resultado["success"]:
                session.pop('carrinho', None) 
                return jsonify({
                    "success": True,
                    "message": "Compra realizada com sucesso!",
                    "venda_id": resultado["venda_id"]
                })
            else:
                return jsonify({"success": False, "message": resultado["message"]}), 400
