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


def abort_if_user_found(id_name):
    session = db_session.create_session()
    current_user = session.query(User).filter(User.id_name == id_name).first()
    if current_user:
        abort(404, message=f"User {id_name} is already registered")


class UserAcc(Resource):
    def post(self):
        args = parser.parse_args()
        if not args.get("username"):
            abort(404, message="Username wasn't sent")
        abort_if_user_found(args["id_name"])
        session = db_session.create_session()
        current_user = User()
        current_user.id_name = args["id_name"]
        current_user.username = args["username"]
        current_user.set_password(args["password"])
        session.add(current_user)
        session.commit()
        return jsonify({"success": True,
                        "id": current_user.id,
                        "created_date": current_user.created_date,
                        "username": current_user.username,
                        "id_name": current_user.id_name})

    def get(self):
        args = parser.parse_args()
        abort_if_user_not_found(args["id_name"])
        session = db_session.create_session()
        current_user = session.query(User).filter(User.id_name == args["id_name"]).first()
        if not current_user.check_password(args["password"]):
            abort(404, message="The password isn't correct")
        return jsonify({"success": True,
                        "id": current_user.id,
                        "created_date": current_user.created_date,
                        "username": current_user.username,
                        "id_name": current_user.id_name})
