from data import db_session
from flask_restful import Resource, abort
from data.user import User
from api.reqparse import table_parser
from flask import jsonify


def abort_if_correct_user_not_found(id_name, user_token):
    session = db_session.create_session()
    correct_user = session.query(User).filter(User.id_name == id_name,
                                              User.user_token == user_token).first()
    if not correct_user:
        return abort(404, message="your token or id_name isn't correct")


class GroupOfTables(Resource):
    def get(self):
        args = table_parser.parse_args()
        abort_if_correct_user_not_found(args["id_name"], args["user_token"])
