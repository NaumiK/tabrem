import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class StatusModel(SqlAlchemyBase):
    __tablename__ = "status"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    order = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    board_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
