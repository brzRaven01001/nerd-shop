from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from back.controllers.cadastro_controller import url
from back.controllers.cadastro_usuario import url_usuario
from back.models.produto import insereProdutoSQL, getProdutos
from back.models.usuario import cadastra_usuario, autentica_usuario
from back.controllers.venda_controller import VendaController
from back.controllers.carrinho_controller import CarrinhoController

app = Flask(__name__)
app.secret_key = 'postgres123'
app.register_blueprint(url)
app.register_blueprint(url_usuario)

venda_controller = VendaController()
carrinho_controller = CarrinhoController()

@app.route("/")
def index():
    produtos = getProdutos()  
    return render_template("index.html", produtos=produtos)

@app.route('/pc')
def pc():
    produtos = getProdutos()  
    return render_template('pc.html', produtos=produtos)

@app.route("/adicionar_carrinho", methods=["POST"])
def adicionar_carrinho():
    try:
        produto_id = int(request.form['produto_id'])
        quantidade = int(request.form.get('quantidade', 1))
        
        resultado_validacao = carrinho_controller.adicionar_ao_carrinho(produto_id, quantidade)
        
        if not resultado_validacao["success"]:
            flash(resultado_validacao["message"], "error")
            return redirect(request.referrer or url_for('index'))
        
        if 'carrinho' not in session:
            session['carrinho'] = []
        
        produto_existente = None
        for item in session['carrinho']:
            if item['produto_id'] == produto_id:
                produto_existente = item
                break
        
        if produto_existente:
            produto_existente['quantidade'] += quantidade
            produto_existente['subtotal'] = produto_existente['preco'] * produto_existente['quantidade']
        else:
            produtos = getProdutos()
            if produto_id < len(produtos):
                produto = produtos[produto_id]
                novo_item = {
                    'produto_id': produto_id,
                    'nome': produto[0],  # nome
                    'preco': float(produto[2]),  # preço
                    'quantidade': quantidade,
                    'imagem_url': produto[5],  # imagem_url
                    'subtotal': float(produto[2]) * quantidade
                }
                session['carrinho'].append(novo_item)
        
        session.modified = True
        flash(f"{resultado_validacao['produto']['nome']} adicionado ao carrinho!", "success")
        
    except Exception as e:
        flash(f"Erro ao adicionar ao carrinho: {str(e)}", "error")
    
    return redirect(request.referrer or url_for('index'))

@app.route("/remover_carrinho", methods=["POST"])
def remover_carrinho():
    try:
        produto_id = int(request.form['produto_id'])
        
        if 'carrinho' in session:
            session['carrinho'] = [item for item in session['carrinho'] if item['produto_id'] != produto_id]
            session.modified = True
            flash("Produto removido do carrinho!", "success")
        
    except Exception as e:
        flash(f"Erro ao remover do carrinho: {str(e)}", "error")
    
    return redirect(url_for('ver_carrinho'))

@app.route("/atualizar_carrinho", methods=["POST"])
def atualizar_carrinho():
    try:
        produto_id = int(request.form['produto_id'])
        nova_quantidade = int(request.form['quantidade'])
        
        if nova_quantidade <= 0:
            return redirect(url_for('remover_carrinho'))
        
        resultado_validacao = carrinho_controller.adicionar_ao_carrinho(produto_id, nova_quantidade)
        
        if not resultado_validacao["success"]:
            flash(resultado_validacao["message"], "error")
            return redirect(url_for('ver_carrinho'))
        
        if 'carrinho' in session:
            for item in session['carrinho']:
                if item['produto_id'] == produto_id:
                    item['quantidade'] = nova_quantidade
                    item['subtotal'] = item['preco'] * nova_quantidade
                    break
            session.modified = True
            flash("Quantidade atualizada!", "success")
        
    except Exception as e:
        flash(f"Erro ao atualizar carrinho: {str(e)}", "error")
    
    return redirect(url_for('ver_carrinho'))

@app.route("/carrinho")
def ver_carrinho():
    carrinho = session.get('carrinho', [])
    total = sum(item['subtotal'] for item in carrinho)
    return render_template("carrinho.html", carrinho=carrinho, total=total)

@app.route("/limpar_carrinho", methods=["POST"])
def limpar_carrinho():
    session.pop('carrinho', None)
    flash("Carrinho limpo!", "success")
    return redirect(url_for('ver_carrinho'))

@app.route("/finalizar_compra", methods=["POST"])
def finalizar_compra():
    try:
        # Verificar se usuário está logado
        if 'usuario' not in session:
            flash("Você precisa estar logado para finalizar a compra!", "error")
            return redirect(url_for('login_usuario'))
        
        # Verificar se carrinho não está vazio
        carrinho = session.get('carrinho', [])
        if not carrinho:
            flash("Seu carrinho está vazio!", "error")
            return redirect(url_for('ver_carrinho'))
        
        # Preparar dados para a compra
        usuario_id = session['usuario'][0]  # Assumindo que ID é o primeiro campo
        itens_compra = []
        
        for item in carrinho:
            itens_compra.append({
                'produto_id': item['produto_id'],
                'quantidade': item['quantidade'],
                'preco_unitario': item['preco']
            })
        
        # Processar compra
        resultado_compra = venda_controller.processar_compra(usuario_id, itens_compra)
        
        if resultado_compra["success"]:
            # Limpar carrinho após compra bem-sucedida
            session.pop('carrinho', None)
            flash(f"Compra realizada com sucesso! ID da venda: {resultado_compra['venda_id']}", "success")
            return redirect(url_for('historico_compras'))
        else:
            flash(resultado_compra["message"], "error")
            return redirect(url_for('ver_carrinho'))
            
    except Exception as e:
        flash(f"Erro ao finalizar compra: {str(e)}", "error")
        return redirect(url_for('ver_carrinho'))

@app.route("/historico_compras")
def historico_compras():
    if 'usuario' not in session:
        flash("Você precisa estar logado para ver o histórico!", "error")
        return redirect(url_for('login_usuario'))
    
    usuario_id = session['usuario'][0]
    resultado = venda_controller.obter_historico_compras(usuario_id)
    
    if resultado["success"]:
        return render_template("historico_compras.html", vendas=resultado["vendas"])
    else:
        flash(resultado["message"], "error")
        return redirect(url_for('index'))

@app.route("/detalhes_venda/<int:venda_id>")
def detalhes_venda(venda_id):
    if 'usuario' not in session:
        flash("Você precisa estar logado!", "error")
        return redirect(url_for('login_usuario'))
    
    usuario_id = session['usuario'][0]
    resultado = venda_controller.obter_detalhes_venda(venda_id, usuario_id)
    
    if resultado["success"]:
        return render_template("detalhes_venda.html", 
                             venda=resultado["venda"], 
                             itens=resultado["itens"])
    else:
        flash(resultado["message"], "error")
        return redirect(url_for('historico_compras'))

@app.route("/comprar_agora", methods=["POST"])
def comprar_produto():
    try:
        produto_id = int(request.form['produto_id'])
        quantidade = int(request.form.get('quantidade', 1))
        
 
        if 'usuario' not in session:
            flash("Você precisa estar logado para comprar!", "error")
            return redirect(url_for('login_usuario'))
        
      
        resultado_validacao = carrinho_controller.adicionar_ao_carrinho(produto_id, quantidade)
        
        if not resultado_validacao["success"]:
            flash(resultado_validacao["message"], "error")
            return redirect(request.referrer or url_for('index'))
        
   
        usuario_id = session['usuario'][0]
        itens_compra = [{
            'produto_id': produto_id,
            'quantidade': quantidade,
            'preco_unitario': resultado_validacao['produto']['preco']
        }]
        
   
        resultado_compra = venda_controller.processar_compra(usuario_id, itens_compra)
        
        if resultado_compra["success"]:
            flash(f"Compra realizada com sucesso! ID: {resultado_compra['venda_id']}", "success")
            return redirect(url_for('historico_compras'))
        else:
            flash(resultado_compra["message"], "error")
            return redirect(request.referrer or url_for('index'))
            
    except Exception as e:
        flash(f"Erro ao processar compra: {str(e)}", "error")
        return redirect(request.referrer or url_for('index'))

@app.route("/cadastro")
def cadastro():
    produtos = getProdutos()  
    return render_template("cadastro.html", produtos=produtos)

@app.route("/cadastro_usuario", methods=["GET", "POST"])
def cadastro_usuario():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        if cadastra_usuario(nome, email, senha):
            return redirect(url_for("login_usuario"))
        else:
            return "Erro ao cadastrar usuário", 500
    return render_template("cadastro_usuario.html")

@app.route("/login_usuario", methods=["GET", "POST"])
def login_usuario():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = autentica_usuario(email, senha)
        
        if usuario:
            session["usuario"] = usuario
            return jsonify({"success": True, "redirect": url_for("index")})
        else:
            return jsonify({"success": False, "message": "Email ou senha incorretos!"})
            
    return render_template("login_usuario.html")

@app.route("/logout")
def logout():
    session.pop('usuario', None)
    session.pop('carrinho', None)
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for('index'))

@app.route("/produto/<int:produto_id>")
def produto_detalhe(produto_id):
    produtos = getProdutos() 
    if produto_id < 0 or produto_id >= len(produtos):
        return "Produto não encontrado", 404
    produto = produtos[produto_id]
    return render_template("produto_detalhe.html", produto=produto)

@app.route('/submit-product', methods=['POST'])
def submit_product():
    nome = request.form.get('product-name')
    descricao = request.form.get('description')
    preco = request.form.get('price')
    categoria = request.form.get('category')
    estoque = request.form.get('stock')
    imagem_url = request.form.get('image-url')
    resultado = insereProdutoSQL(nome, descricao, preco, categoria, estoque, imagem_url)
    
    if resultado and "error" in resultado:
        return f"Erro ao cadastrar produto: {resultado['error']}", 500
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)