from flask import Blueprint, request, jsonify, render_template, url_for, redirect
from back.models.produto import insereProdutoSQL

url = Blueprint("app_pb", __name__)


@url.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


