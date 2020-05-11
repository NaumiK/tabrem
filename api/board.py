from data import db_session
from data.board import BoardModel
from flask_restful import Resource, abort
from api.reqparse import table_parser
from flask import jsonify
from api.token import abort_if_token_is_not_correct
from api.task import TaskModel
from api.status import StatusModel
from api.user import check_author, check_password_for_args


class Board(Resource):
    def post(self, id_name):
        # region work with args
        args = table_parser.parse_args()
        abort_if_token_is_not_correct(id_name, args["user_token"])
        check_password_for_args(id_name, args["password"])
        # endregion

        session = db_session.create_session()
        new_table = BoardModel()
        new_table.name = args["name"]
        new_table.description = args["description"]
        new_table.author_id = id_name
        session.add(new_table)
        session.commit()

        response = {
            "message": "success",
            "id": new_table.id
        }
        return jsonify(response)

    def get(self, id_name):
        # region work with args
        args = table_parser.parse_args()
        abort_if_token_is_not_correct(id_name, args["user_token"])
        check_password_for_args(id_name, args["password"])
        # endregion

        session = db_session.create_session()

        response = {
            "board": [],
            "message": "success"
        }
        # list of objects
        if not args["id"]:
            current_board = session.query(BoardModel).filter(BoardModel.author_id == id_name).all()
            if not current_board:
                return abort(404, message="Not found")
            for i in current_board:
                response["board"].append({
                    "name": i.name,
                    "id": i.id,
                    "description": i.description
                })
        # one object
        else:
            check_author(id_name, args["id"], BoardModel)
            current_board = session.query(BoardModel).filter(BoardModel.id == args["id"]).first()
            response["board"] = {
                "id": current_board.id,
                "name": current_board.name,
                "description": current_board.description
            }

        return jsonify(response)

    def delete(self, id_name):
        # region work with args
        args = table_parser.parse_args()
        abort_if_token_is_not_correct(id_name, args["user_token"])
        check_password_for_args(id_name, args["password"])
        # endregion

        session = db_session.create_session()
        # one element
        if args["id"]:
            check_author(id_name, args["id"], BoardModel)
            boards = session.query(BoardModel).filter(BoardModel.id == args["id"]).all()
        # group of elements
        else:
            boards = session.query(BoardModel).filter(BoardModel.author_id == id_name).all()
            if not boards:
                return abort(404, message="Not found")
        for board in boards:
            for i in session.query(TaskModel).filter(TaskModel.board_id == board.id).all():
                session.delete(i)
            for i in session.query(StatusModel).filter(StatusModel.board_id == board.id).all():
                session.delete(i)
            session.delete(board)
        session.commit()

        response = {
            "message": "success"
        }

        return jsonify(response)

    def put(self, id_name):
        # region work with args
        args = table_parser.parse_args()
        abort_if_token_is_not_correct(id_name, args["user_token"])
        check_password_for_args(id_name, args["password"])
        if not args["id"]:
            return abort(404, message="You missed id argument")
        # endregion

        check_author(id_name, args["id"], BoardModel)
        session = db_session.create_session()
        current_board = session.query(BoardModel).filter(BoardModel.id == args["id"]).first()
        if args["name"]:
            current_board.name = args["name"]
        if args["description"]:
            current_board.description = args["description"]
        session.commit()

        response = {
            "message": "success"
        }
        return jsonify(response)
