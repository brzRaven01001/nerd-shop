from flask import Flask, render_template
from back.controllers.cadastro_controller import url

app = Flask(__name__)
app.register_blueprint(url)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/pc')
def pc():
    return render_template('pc.html')



if __name__ == "__main__":
    app.run(debug=True)