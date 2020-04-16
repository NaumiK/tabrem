from flask import Blueprint, render_template, redirect
from data.user import User
from data import db_session
from reg_login.forms import RegisterForm
from requests import post, get
from flask_login import login_user

register = Blueprint("register", __name__,
                     template_folder="templates")


# @register.route("/register", methods=["GET", "POST"])
# def registration():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         session = db_session.create_session()
#         in_base = session.query(User).filter(form.id_name.data == User.id_name).first()
#         if in_base:
#             return render_template("register.html", message="Идентификационное имя уже присутсвует в базе",
#                                    form=form)
#         if form.password.data != form.password_again.data:
#             return render_template('register.html', title='Регистрация',
#                                    form=form,
#                                    message="Пароли не совпадают")
#         current_user = User()
#         current_user.id_name = form.id_name.data
#         current_user.username = form.username.data
#         current_user.set_password(form.password.data)
#         session.add(current_user)
#         session.commit()
#         login_user(current_user, True)
#         return redirect("/")
#     return render_template('register.html', title='Регистрация', form=form, _in_=False, name="")


@register.route("/register", methods=["GET", "POST"])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        params = {
            'idname': form.id_name.data,
            'password': form.password.data,
            'username': form.username.data
        }
        print(post('http://localhost:8080/api/register', json=params).json())
    return render_template('register.html', title='Регистрация', form=form)
