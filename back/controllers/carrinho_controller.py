from back.models.produto import getProdutos

class CarrinhoController:
    
    def adicionar_ao_carrinho(self, produto_id, quantidade=1):
        """Valida se pode adicionar produto ao carrinho"""
        try:
            produtos = getProdutos()
            
            # Encontrar produto
            produto_encontrado = None
            for produto in produtos:
                if produto[0] == produto_id:  # Ajuste
                    produto_encontrado = produto
                    break
            
            if not produto_encontrado:
                return {"success": False, "message": "Produto não encontrado"}
            
            # Extrair dados (ajuste)
            estoque = produto_encontrado[4]
            preco = float(produto_encontrado[2])
            nome = produto_encontrado[0]
            
            if estoque < quantidade:
                return {
                    "success": False, 
                    "message": f"Estoque insuficiente para {nome}. Disponível: {estoque}"
                }
            
            return {
                "success": True,
                "message": "Produto pode ser adicionado ao carrinho",
                "produto": {
                    'produto_id': produto_id,
                    'nome': nome,
                    'preco': preco,
                    'quantidade': quantidade,
                    'subtotal': preco * quantidade
                }
            }
            
        except Exception as e:
            return {"success": False, "message": f"Erro ao validar produto: {str(e)}"}