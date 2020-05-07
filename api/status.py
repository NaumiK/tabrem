from data import db_session
from data.board import BoardModel
from data.status import StatusModel
from flask_restful import Resource, abort
from api.reqparse import status_parser
from flask import jsonify
from api.token import abort_if_token_is_not_correct
from data.task import TaskModel
from api.user import check_author


def abort_if_table_not_found(board_id):
    session = db_session.create_session()
    if not session.query(BoardModel).filter(BoardModel.id == board_id).first():
        return abort(404, message="Table not found")


class Status(Resource):
    def post(self, id_name, board_id):
        # region work with args
        abort_if_table_not_found(board_id)
        args = status_parser.parse_args()
        if not args["order"]:
            return abort(404, message="You missed order argument")
        abort_if_token_is_not_correct(id_name, args["user_token"])
        if int(args["order"]) <= 0:
            return abort(404, message="Order should be larger than zero")
        # endregion

        session = db_session.create_session()
        current_status = StatusModel()
        current_status.board_id = board_id
        current_status.author_id = id_name
        current_status.name = args["name"]
        current_status.order = args["order"]
        # make a step for upper order (2 -> [1, 2, 3] = [1, 2, 3, 4])
        bigger_order = session.query(StatusModel).filter(StatusModel.board_id == current_status.board_id,
                                                         StatusModel.order >= current_status.order).all()
        for i in bigger_order:
            i.order += 1
        session.add(current_status)
        session.commit()

        response = {
            "message": "success",
            "id": current_status.id
        }
        return jsonify(response)

    def get(self, id_name, board_id):
        # region work with args
        abort_if_table_not_found(board_id)
        args = status_parser.parse_args()
        abort_if_token_is_not_correct(id_name, args["user_token"])
        # endregion

        session = db_session.create_session()
        response = {
            "status": [],
            "message": "success"
        }
        # list of objects
        if not args["id"]:
            check_author(id_name, board_id, BoardModel)
            current_statuses = session.query(StatusModel).filter(StatusModel.board_id == board_id).all()
            for i in current_statuses:
                response["status"].append({
                    "id": i.id,
                    "order": i.order,
                    "name": i.name
                })
        # one object
        else:
            check_author(id_name, args["id"], StatusModel)
            current_status = session.query(StatusModel).filter(StatusModel.id == args["id"]).first()
            if not current_status:
                return abort(404, message="Status not found")
            response["status"] = {
                "id": current_status.id,
                "name": current_status.name,
                "order": current_status.order
            }
        return jsonify(response)

    def delete(self, id_name, board_id):
        # region work with args
        abort_if_table_not_found(board_id)
        args = status_parser.parse_args()
        abort_if_token_is_not_correct(id_name, args["user_token"])
        # endregion

        session = db_session.create_session()
        status_for_delete = session.query(StatusModel).filter(StatusModel.id == args["id"]).first()
        for i in session.query(StatusModel).filter(StatusModel.board_id == status_for_delete.board_id,
                                                   StatusModel.order > status_for_delete.order).all():
            i.order -= 1
        check_author(id_name, status_for_delete.id, StatusModel)
        for i in session.query(TaskModel).filter(TaskModel.status_id == status_for_delete.id).all():
            session.delete(i)
        session.delete(status_for_delete)
        session.commit()

        response = {
            "message": "success"
        }
        return jsonify(response)

    def put(self, id_name, board_id):
        # region work with args
        abort_if_table_not_found(board_id)
        args = status_parser.parse_args()
        if not args["id"]:
            return abort(404, message="You missed id argument")
        abort_if_token_is_not_correct(id_name, args["user_token"])
        # endregion

        check_author(id_name, args["id"], StatusModel)
        session = db_session.create_session()
        current_status = session.query(StatusModel).filter(StatusModel.id == args["id"]).first()
        if args["name"]:
            current_status.name = args["name"]
        # region order move
        if args["order"]:
            if current_status.order < int(args["order"]):
                selected_statuses = session.query(StatusModel).filter(StatusModel.board_id == current_status.board_id,
                                                                      StatusModel.order > current_status.order,
                                                                      StatusModel.order <= args["order"]).all()
                for i in selected_statuses:
                    i.order -= 1
                current_status.order = args["order"]
            else:
                selected_statuses = session.query(StatusModel).filter(StatusModel.board_id == current_status.board_id,
                                                                      StatusModel.order < current_status.order,
                                                                      StatusModel.order >= args["order"]).all()
                for i in selected_statuses:
                    i.order += 1
                current_status.order = args["order"]
        # endregion
        session.commit()

        response = {
            "message": "success"
        }
        return jsonify(response)
