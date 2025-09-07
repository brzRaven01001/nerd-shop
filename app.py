from flask import Flask, render_template
from controllers.cadastro_controller import url

app = Flask(__name__)
app.register_blueprint(url)


def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)