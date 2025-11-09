from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from back.controllers.cadastro_controller import url
from back.controllers.cadastro_usuario import url_usuario
from back.models.produto import insereProdutoSQL, getProdutos
from back.models.usuario import cadastra_usuario, autentica_usuario
from back.controllers.venda_controller import VendaController, executar_venda_controller
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

        # Pega todos os produtos do banco
        produtos = getProdutos()
        print("Produto ID recebido:", produto_id)
        print("IDs do banco:", [p[6] for p in produtos])

        # Busca o produto no banco antes de qualquer coisa
        produto = next((p for p in produtos if int(p[6]) == produto_id), None)
   
        # Agora podemos chamar o controller, se necessário
        resultado_validacao = carrinho_controller.adicionar_ao_carrinho(produto_id, quantidade)
        if not resultado_validacao["success"]:
            flash(resultado_validacao["message"], "error")
            return redirect(request.referrer or url_for('index'))

        # Inicializa carrinho na sessão se não existir
        if 'carrinho' not in session:
            session['carrinho'] = []

        # Verifica se o produto já existe no carrinho
        produto_existente = next((i for i in session['carrinho'] if i['produto_id'] == produto_id), None)

        if produto_existente:
            produto_existente['quantidade'] += quantidade
            produto_existente['subtotal'] = produto_existente['preco'] * produto_existente['quantidade']
        else:
            novo_item = {
                'produto_id': produto_id,
                'nome': produto[0],
                'preco': float(produto[2]),
                'quantidade': quantidade,
                'imagem_url': produto[5],
                'subtotal': float(produto[2]) * quantidade
            }
            session['carrinho'].append(novo_item)

        session.modified = True
        flash(f"{produto[0]} adicionado ao carrinho!", "success")

    except Exception as e:
        flash(f"Erro ao adicionar ao carrinho: {str(e)}", "error")

    return redirect(request.referrer or url_for('index'))


@app.route("/carrinho")
def ver_carrinho():
    carrinho = session.get('carrinho', [])
    total = sum(item['subtotal'] for item in carrinho)
    return render_template("carrinho.html", carrinho=carrinho, total=total)


@app.route("/remover_item_carrinho", methods=["POST"])
def remover_item_carrinho():
    try:
        produto_id = int(request.form['produto_id'])
        if 'carrinho' in session:
            session['carrinho'] = [item for item in session['carrinho'] if item['produto_id'] != produto_id]
            session.modified = True
            flash("Produto removido do carrinho!", "success")
    except Exception as e:
        flash(f"Erro ao remover item: {str(e)}", "error")
    return redirect(url_for('ver_carrinho'))


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
    produto = next((p for p in produtos if int(p[6]) == produto_id), None)
    print(f"Produto ID recebido: {produto_id}") 
    if not produto:
        return "Produto não achado", 404
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


@app.route("/executar_venda", methods=["POST"])
def executar_venda():
    return executar_venda_controller()

@app.route("/confirmacao")
def confirmacao():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)