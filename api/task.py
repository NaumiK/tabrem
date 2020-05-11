from data import db_session
from api.reqparse import task_parser
from flask_restful import Resource, abort
from api.token import abort_if_token_is_not_correct
from data.task import TaskModel
from api.status import StatusModel
from flask import jsonify
from api.user import check_author, check_password_for_args


def abort_if_status_not_found(board_id):
    session = db_session.create_session()
    if not session.query(StatusModel).filter(StatusModel.id == board_id).first():
        return abort(404, message="Status not found")


class Task(Resource):
    def post(self, id_name, board_id, status_id):
        # region work with args
        args = task_parser.parse_args()
        abort_if_token_is_not_correct(id_name, args["user_token"])
        check_password_for_args(id_name, args["password"])
        # endregion

        session = db_session.create_session()
        current_task = TaskModel()
        current_task.name = args["name"]
        current_task.description = args["description"]
        current_task.author_id = id_name
        current_task.board_id = board_id
        current_task.status_id = status_id
        session.add(current_task)
        session.commit()

        response = {
            "message": "success"
        }
        return jsonify(response)

    def get(self, id_name, board_id, status_id):
        # region work with args
        args = task_parser.parse_args()
        abort_if_token_is_not_correct(id_name, args["user_token"])
        check_password_for_args(id_name, args["password"])
        # endregion

        session = db_session.create_session()
        response = {
            "task": [],
            "message": "success"
        }
        # list of objects
        if not args["id"]:
            check_author(id_name, status_id, StatusModel)
            current_task = session.query(TaskModel).filter(TaskModel.status_id == status_id).all()
            for i in current_task:
                response["task"].append({
                    "id": i.id,
                    "name": i.name,
                    "description": i.description
                })
        # one object
        else:
            check_author(id_name, args["id"], TaskModel)
            current_task = session.query(TaskModel).filter(TaskModel.id == args["id"]).first()
            response["task"] = {
                "id": current_task.id,
                "name": current_task.name,
                "description": current_task.description
            }
        return jsonify(response)

    def delete(self, id_name, board_id, status_id):
        # region work with args
        args = task_parser.parse_args()
        abort_if_token_is_not_correct(id_name, args["user_token"])
        check_password_for_args(id_name, args["password"])
        # endregion

        session = db_session.create_session()
        if args["id"]:
            check_author(id_name, args["id"], TaskModel)
            current_task = session.query(TaskModel).filter(args["id"] == TaskModel.id).first()
            session.delete(current_task)
        else:
            for task in session.query(TaskModel).filter(status_id == TaskModel.id, TaskModel.author_id == id_name):
                session.delete(task)
        session.commit()

        response = {
            "message": "success"
        }
        return jsonify(response)

    def put(self, id_name, board_id, status_id):
        # region work with args
        args = task_parser.parse_args()
        abort_if_token_is_not_correct(id_name, args["user_token"])
        check_password_for_args(id_name, args["password"])
        if not args["id"]:
            return abort(404, message="You missed id argument")
        # endregion

        check_author(id_name, args["id"], TaskModel)
        session = db_session.create_session()
        current_task = session.query(TaskModel).filter(TaskModel.id == args["id"]).first()
        current_task.name = args["name"]
        current_task.description = args["description"]
        session.commit()

        response = {
            "message": "success"
        }
        return jsonify(response)
