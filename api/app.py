from flask import Flask, jsonify, request
from flask.helpers import make_response
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import bcrypt

app = Flask(__name__)
api = Api(app)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)


class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    owner = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'Todo(id = {self.id}, content = {self.content}, owner = {self.owner})'


class UserModel(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    passwordHash = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'User(uid = {self.uid}, username = {self.username}, passwordHash = {self.passwordHash})'

# db.drop_all()
# db.create_all()

# todo = TodoModel(content="I need to study", owner='Tom')
# db.session.add(todo)
# todo = TodoModel(content="I need to poop", owner='Dick')
# db.session.add(todo)

# hashed = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt())
# user = UserModel(username="Tom", passwordHash=hashed)
# db.session.add(user)
# hashed = bcrypt.hashpw('test'.encode('utf-8'), bcrypt.gensalt())
# user = UserModel(username="test", passwordHash=hashed)
# db.session.add(user)

# db.session.commit()


todo_new_args = reqparse.RequestParser()
todo_new_args.add_argument(
    'content', type=str, help='Todo cannot be empty', required=True)
todo_new_args.add_argument(
    'owner', type=str, help='User must be logged in', required=True)


def todo_serializer(todo):
    return{'id': todo.id, 'content': todo.content, 'owner': todo.owner}


def user_serializer(user):
    return{'uid': user.uid, 'username': user.username, 'password': user.passwordHash.decode('utf-8')}


class TodoList(Resource):
    def get(self):
        return jsonify([*map(todo_serializer, TodoModel.query.all())])

    def post(self):
        args = todo_new_args.parse_args()
        todo = TodoModel(content=args['content'], owner=args['owner'])
        db.session.add(todo)
        db.session.commit()
        return todo_serializer(todo), 201


class Todo(Resource):
    @jwt_required
    def get(self, todo_id):
        result = TodoModel.query.filter_by(id=todo_id).first()
        if not result:
            abort(404, message='Todo not found...')
        return jsonify(todo_serializer(result))

    def delete(self, todo_id):
        result = TodoModel.query.filter_by(id=todo_id).first()
        if not result:
            abort(404, message='Todo not found...')
        TodoModel.query.filter_by(id=todo_id).delete()
        db.session.commit()
        return {'204': 'Deleted successfully'}


login_args = reqparse.RequestParser()
login_args.add_argument(
    'username', type=str, help='Username cannot be empty', required=True)
login_args.add_argument(
    'password', type=str, help='Password must be logged in', required=True)


class UserLogin(Resource):
    def get(self):
        return (jsonify([*map(user_serializer, UserModel.query.all())]))

    def post(self):
        args = login_args.parse_args()
        username = args['username']
        password = args['password']

        user = UserModel.query.filter_by(username=username).first()

        if not bcrypt.checkpw(password.encode('utf-8'), user.passwordHash):
            abort(404, message="User not found...")

        access_token = create_access_token(identity=username)
        return make_response(jsonify(access_token=access_token), 200)


class UserRegister(Resource):
    def post(self):
        args = login_args.parse_args()
        username = args['username']
        password = args['password']

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = UserModel(username=username, passwordHash=hashed)
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=username)

        return make_response(jsonify(message='User has been created', access_token=access_token), 200)


api.add_resource(TodoList, '/')
api.add_resource(Todo, '/todo/<int:todo_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run()
