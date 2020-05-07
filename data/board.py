import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class BoardModel(SqlAlchemyBase):
    __tablename__ = "board"

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    description = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
