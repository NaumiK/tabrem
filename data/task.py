import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class TaskModel(SqlAlchemyBase):
    __tablename__ = "tasks"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    status_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    board_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

