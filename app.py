from flask import  Flask, render_template, request, redirect, url_for, session, flash
from back.controllers.cadastro_controller import url
from back.models.model import insereProdutoSQL, getProdutos



app = Flask(__name__)
app.secret_key = 'Semsenh4?'
app.register_blueprint(url)



@app.route("/")
def index():
    produtos = getProdutos()  # pega todos os produtos cadastrados
    return render_template("index.html", produtos=produtos)

@app.route('/pc')
def pc():
    return render_template('pc.html')

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

@app.route("/produto/<int:produto_id>")
def produto_detalhe(produto_id):
    produtos = getProdutos()  # sua função que retorna todos os produtos
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