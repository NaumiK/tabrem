from flask import Flask, render_template
from flask_restful import Api
from flask_login import LoginManager
from data import db_session
from data.user import User
from pages import login, register, client_page
from api import reg_login, tables

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
    api.add_resource(reg_login.UserAcc, '/api/useracc')
    api.add_resource(tables.Test, '/api/tables')
    app.run("127.0.0.1", port=8080)
