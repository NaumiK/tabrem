from flask import Blueprint
from flask import render_template
from data.user import User
from data import db_session
from flask_wtf import FlaskForm
from flask import redirect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_login import login_user


register = Blueprint("register", __name__,
                      template_folder="templates")


class FormRegistration(FlaskForm):
    id_name = StringField("ID name", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Повторите пароль", validators=[DataRequired()])
    username = StringField("Имя пользователя", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироватьтся")


@blueprint.route("/register", methods=["GET", "POST"])
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
        login_user(current_user, True)
        return redirect("/")
    return render_template('register.html', title='Регистрация', form=form, _in_=False, name="")
