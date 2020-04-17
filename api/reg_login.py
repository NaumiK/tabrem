from flask_restful import Resource, abort
from data import db_session
from data.user import User
from api.reqparse import parser
from flask import jsonify


def abort_if_user_not_found(id_name):
    session = db_session.create_session()
    current_user = session.query(User).filter(id_name == User.id_name).first()
    if not current_user:
        abort(404, message=f"User with {id_name} id name not found")
        return False
    return True


class Register(Resource):
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if session.query(User).filter(User.id_name == args["idname"]).first():
            abort(404, message=f"User {args['idname']} is already registered")
        current_user = User()
        current_user.id_name = args["idname"]
        current_user.username = args["username"]
        current_user.set_password(args["password"])
        session.add(current_user)
        session.commit()
        return jsonify({"success": True})


class Login(Resource):
    def get_post(self):
        pass

    def post(self):
        pass
