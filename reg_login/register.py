from flask import Blueprint, render_template, redirect
from data.user import User
from reg_login.forms import RegisterForm
from requests import post
from flask_login import login_user

register = Blueprint("register", __name__,
                     template_folder="templates")


@register.route("/register", methods=["GET", "POST"])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        params = {
            'id_name': form.id_name.data,
            'password': form.password.data,
            'username': form.username.data
        }
        response = post('http://localhost:8080/api/useracc', json=params).json()
        print(response)
        if form.password.data != form.password_again.data:
            return render_template("register.html", message="Passwords must be the same", form=form)
        elif not response.get('success', False):
            return render_template("register.html", message=response.get('message', 'Error'), form=form)
        current_user = User()
        current_user.id_name = response["id_name"]
        current_user.username = response["username"]
        current_user.id = response["id"]
        print(current_user)
        login_user(current_user, remember=True)
        return redirect("/")
    return render_template('register.html', title='Регистрация', form=form)
