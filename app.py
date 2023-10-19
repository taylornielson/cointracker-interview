from flask import Flask
from api import api

app = Flask(__name__)
app.config['RESTX_VALIDATE'] = True
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=5001)