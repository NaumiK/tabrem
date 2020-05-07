from flask_restful import Resource, abort
from data import db_session
from data.user import User
from api.reqparse import reg_login_parser
from flask import jsonify
from api.token import generate_token


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


def check_author(id_name, object_id, model):
    session = db_session.create_session()
    if not session.query(model).filter(model.author_id == id_name, model.id == object_id).first():
        return abort(404, message="Not found")


class UserAcc(Resource):
    def post(self):
        # region work with args
        args = reg_login_parser.parse_args()
        if not args.get("username"):
            abort(404, message="Username wasn't sent")
        # endregion

        abort_if_user_found(args["id_name"])

        session = db_session.create_session()
        current_user = User()
        current_user.id_name = args["id_name"]
        current_user.username = args["username"]
        current_user.user_token = generate_token()
        current_user.set_password(args["password"])
        session.add(current_user)
        session.commit()

        response = {"message": "success",
                    "id": current_user.id,
                    "created_date": current_user.created_date,
                    "username": current_user.username,
                    "id_name": current_user.id_name,
                    "user_token": current_user.user_token}
        return jsonify(response)

    def get(self):
        # region work with args
        args = reg_login_parser.parse_args()
        # endregion

        abort_if_user_not_found(args["id_name"])

        session = db_session.create_session()
        current_user = session.query(User).filter(User.id_name == args["id_name"]).first()
        if not current_user.check_password(args["password"]):
            abort(404, message="The password isn't correct")

        response = {"message": "success",
                    "id": current_user.id,
                    "created_date": current_user.created_date,
                    "username": current_user.username,
                    "id_name": current_user.id_name,
                    "user_token": current_user.user_token}
        return jsonify(response)
