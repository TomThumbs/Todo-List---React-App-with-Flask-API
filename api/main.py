from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields,marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.debug = True
db = SQLAlchemy(app)


if __name__ == "__main__":
    app.run()