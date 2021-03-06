from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


if __name__ == '__main__':
    app.run(debug=True)