from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

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
        return f'Todo(id = {self.id}, content = {self.content}, owner = {self.owner}'


# db.create_all()


# todo = TodoModel(content="I need to study", owner='Tom')
# db.session.add(todo)
# todo = TodoModel(content="I need to poop", owner='Dick')
# db.session.add(todo)

# db.session.commit()

todo_new_args = reqparse.RequestParser()
todo_new_args.add_argument(
    'content', type=str, help='Todo cannot be empty', required=True)
todo_new_args.add_argument(
    'owner', type=str, help='User must be logged in', required=True)


def todo_serializer(todo):
    return{'id': todo.id, 'content': todo.content, 'owner': todo.owner}


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


class UserLogin(Resource):
    def post(self):
        username = request.form['username']
        password = request.form['password']
        if not username:
            abort(400, message="Missing username")
        if not password:
            abort(400, message="Missing password")

        if username != 'test' or password != 'test':
            return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=username)

        return {}


api.add_resource(TodoList, '/')
api.add_resource(Todo, '/<int:todo_id>')

if __name__ == "__main__":
    app.run()
