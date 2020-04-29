from flask_restful import Resource, abort
from data import db_session
from data.user import User
from api.reqparse import reg_login_parser
from flask import jsonify
import random


def generate_token():
    session = db_session.create_session()
    token = ''.join([chr(random.randint(38, 122)) for _ in range(random.randint(20, 40))])
    current_user_token = session.query(User).filter(User.user_token == token).first()
    if current_user_token:
        generate_token()
    return token


def abort_if_user_not_found(id_name):
    session = db_session.create_session()
    current_user = session.query(User).filter(id_name == User.id_name).first()
    if not current_user:
        abort(404, message=f"User with {id_name} id name not found")


def abort_if_user_found(id_name):
    session = db_session.create_session()
    current_user = session.query(User).filter(User.id_name == id_name).first()
    if current_user:
        abort(404, message=f"User {id_name} is already registered")


class UserAcc(Resource):
    def post(self):
        args = reg_login_parser.parse_args()
        if not args.get("username"):
            abort(404, message="Username wasn't sent")
        abort_if_user_found(args["id_name"])
        session = db_session.create_session()
        current_user = User()
        current_user.id_name = args["id_name"]
        current_user.username = args["username"]
        current_user.user_token = generate_token()
        current_user.set_password(args["password"])
        session.add(current_user)
        session.commit()
        return jsonify({"success": True,
                        "id": current_user.id,
                        "created_date": current_user.created_date,
                        "username": current_user.username,
                        "id_name": current_user.id_name,
                        "user_token": current_user.user_token})

    def get(self):
        args = reg_login_parser.parse_args()
        abort_if_user_not_found(args["id_name"])
        session = db_session.create_session()
        current_user = session.query(User).filter(User.id_name == args["id_name"]).first()
        if not current_user.check_password(args["password"]):
            abort(404, message="The password isn't correct")
        return jsonify({"success": True,
                        "id": current_user.id,
                        "created_date": current_user.created_date,
                        "username": current_user.username,
                        "id_name": current_user.id_name,
                        "user_token": current_user.user_token})
