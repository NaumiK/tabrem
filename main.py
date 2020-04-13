from flask import Flask, render_template
from flask_restful import Api
from flask_login import LoginManager
from data import db_session
from flask_wtf import FlaskForm
from flask import redirect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from data.user import User

app = Flask(__name__)
api = Api(app)
app.config["SECRET_KEY"] = "KwfEece8LFeKmvrkpjuk5nNKaibEwv"
login_manager = LoginManager()
login_manager.init_app(app)


class FormRegistration(FlaskForm):
    id_name = StringField("ID name", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Повторите пароль", validators=[DataRequired()])
    username = StringField("Имя пользователя", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироватьтся")


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
              "name": "Daniil"}
    return render_template("table_page.html", **params)


@app.route("/register", methods=["GET", "POST"])
def registration():
    form = FormRegistration()
    if form.validate_on_submit():
        session = db_session.create_session()
        in_base = session.query(User).filter(form.id_name.data == User.id_name).first()
        if in_base:
            return render_template("register.html", message="Идентификационное имя уже присутсвует в базе",
                                   form=form)
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        current_user = User()
        current_user.id_name = form.id_name.data
        current_user.username = form.username.data
        current_user.set_password(form.password.data)
        session.add(current_user)
        session.commit()
        return redirect("/")
    return render_template('register.html', title='Регистрация', form=form, _in_=False, name="")


if __name__ == '__main__':
    db_session.global_init("db/tablets.sqlite")
    app.run()
