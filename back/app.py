from flask import Flask
from controllers.cadastro_controller import *

app = Flask(__name__)
app.register_blueprint(url)

if __name__ == "__main__":
    app.run(debug=True)
