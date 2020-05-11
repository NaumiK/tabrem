from flask import Flask, render_template
from flask_restful import Api
from flask_login import LoginManager
from data import db_session
from data.user import User
from pages import login, register, client_page
from api import user, status, board, task

app = Flask(__name__)
api = Api(app)
app.config["SECRET_KEY"] = "KwfEece8LFeKmvrkpjuk5nNKaibEwv"
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/")
@app.route("/tablets")
@app.route("/people")
def main():
    params = {"title": "TabRem",
              "_in_": False,
              "name": "something"}
    return render_template("table_page.html", **params)


if __name__ == '__main__':
    db_session.global_init("db/tablets.sqlite")
    app.register_blueprint(register.register)
    app.register_blueprint(login.login)
    app.register_blueprint(client_page.client_page)
    api.add_resource(user.UserAcc, '/api/useracc')
    api.add_resource(board.Board, '/api/<string:id_name>/board')
    api.add_resource(status.Status, '/api/<string:id_name>/board/<string:board_id>')
    api.add_resource(task.Task, '/api/<string:id_name>/board/<string:board_id>/<string:status_id>')
    app.run()
