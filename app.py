from flask import  Flask, render_template, request, redirect, url_for, session, flash
from back.controllers.cadastro_controller import url
from back.controllers.cadastro_usuario import url_usuario
from back.models.produto import insereProdutoSQL, getProdutos
from back.models.usuario import cadastra_usuario, autentica_usuario


app = Flask(__name__)
app.secret_key = 'postgres123'
app.register_blueprint(url)
app.register_blueprint(url_usuario)

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
    produto_id = int(request.form['produto_id'])
    produto = getProdutos()[produto_id]
    if 'carrinho' not in session:
        session['carrinho'] = []
    session['carrinho'].append(produto)
    flash(f"{produto[0]} adicionado ao carrinho!")
    return redirect(url_for('index'))

@app.route("/comprar_produto", methods=["POST"])
def comprar_produto():
    produto_id = int(request.form['produto_id'])
    produto = getProdutos()[produto_id]
    flash(f"Compra iniciada para {produto[0]}!")
    return redirect(url_for('index'))

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
            return redirect(url_for("cadastro_usuario"))
        else:
            return "Erro ao cadastrar usuário", 500
    return render_template("cadastro_usuario.html")

@app.route("/login_usuario", methods=["GET", "POST"])
def login_usuario():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form
        usuario = autentica_usuario(email, senha)
        if usuario:
            session["usuario"] = usuario
            return redirect(url_for("index"))
        else:
            return "Email ou senha incorretos!"
    return render_template("login_usuario.html")



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