from flask import  Flask, render_template, request, redirect, url_for
from back.controllers.cadastro_controller import url
from back.models.model import insereProdutoSQL
app = Flask(__name__)
app.register_blueprint(url)



@app.route("/")
def index():
    return render_template("index.html")

@app.route('/pc')
def pc():
    return render_template('pc.html')



@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


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