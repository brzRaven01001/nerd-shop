from flask import Blueprint, request, jsonify
from models import model

# define o blueprint
url = Blueprint("app_pb", __name__)

#rotas de cadastro
@url.route("/produto", methods=["POST"])
def post_produto():
    try:
        data = request.get_json()  
        nome = data.get("nome")
        descricao = data.get("descricao")
        preco = data.get("preco")
        categoria = data.get("categoria")
        estoque = data.get("estoque")
        imagem_url = data.get("imagem_url")

        response = model.insereProdutoSQL(nome, descricao, preco, categoria, estoque, imagem_url)
        return jsonify(response), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
