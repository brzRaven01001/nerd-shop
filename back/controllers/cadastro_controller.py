from flask import Blueprint, request, jsonify, render_template
from models import model

url = Blueprint("app_pb", __name__)
@url.route("/cadastro")
def cadastro_page():
    return render_template("cadastro.html")



@url.route("/submit-product", methods=["POST"])
def post_produto():
    try:
        nome = request.form.get("product-name")
        descricao = request.form.get("description")
        preco = request.form.get("price")
        categoria = request.form.get("category")
        estoque = request.form.get("stock")
        imagem_url = request.form.get("image-url")

        response = model.insereProdutoSQL(nome, descricao, preco, categoria, estoque, imagem_url)
        return jsonify(response), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500