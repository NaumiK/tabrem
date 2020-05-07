from flask import Blueprint, render_template, redirect
from data.user import User
from pages.forms import RegisterForm
from requests import post
from flask_login import login_user, current_user

register = Blueprint("register", __name__,
                     template_folder="templates")


@register.route("/register", methods=["GET", "POST"])
def registration():
    if current_user.is_authenticated:
        return redirect("/client_page")
    form = RegisterForm()
    if form.validate_on_submit():
        params = {
            'id_name': form.id_name.data,
            'password': form.password.data,
            'username': form.username.data
        }
        response = post('http://localhost:8080/api/useracc', json=params).json()
        if form.password.data != form.password_again.data:
            return render_template("register.html", message="Passwords must be the same", form=form)
        elif response["message"] != "success":
            return render_template("register.html", message=response.get('message', 'Error'), form=form)
        _user = User()
        _user.id_name = response["id_name"]
        _user.username = response["username"]
        _user.id = response["id"]
        login_user(_user, remember=True)
        return redirect("/client_page")
    return render_template('register.html', title='Регистрация', form=form)
