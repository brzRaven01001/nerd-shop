from flask import Blueprint, request, redirect, url_for, render_template, session, jsonify
from back.models.usuario import cadastra_usuario, autentica_usuario

url_usuario = Blueprint("url_usuario", __name__)

@url_usuario.route("/cadastro-usuario", methods=["POST"])
def post_user():
    try:
        data = request.get_json(force=True)
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')
        if not all([nome, email, senha]):
            return jsonify({"error": "Dados JSON necessários"}), 400
            
        
        success = cadastra_usuario(nome, email, senha)
        
        if success:
            return jsonify({"message": "Usuário cadastrado com sucesso"}), 201
        else:
            return jsonify({"error": "Erro ao cadastrar usuário"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500



@url_usuario.route("/login-usuario", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = autentica_usuario(email, senha)
        if usuario:
            session["usuario"] = usuario
            return redirect(url_for("index"))
        else:
            return "Email ou senha incorretos!"
    return render_template("login_usuario.html")

@url_usuario.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("index"))