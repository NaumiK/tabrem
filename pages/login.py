from flask import Blueprint, redirect, render_template
from .forms import LoginForm
from data.user import User
from requests import get
from flask_login import login_user, current_user

login = Blueprint("login", __name__,
                  template_folder="templates")


@login.route("/login", methods=["GET", "POST"])
def login_func():
    if current_user.is_authenticated:
        return redirect("/client_page")
    form = LoginForm()
    if form.validate_on_submit():
        params = {
            "id_name": form.id_name.data,
            "password": form.password.data
        }
        response = get("http://localhost:8080/api/useracc", json=params).json()
        if response["message"] != "success":
            return render_template("login.html", title="Вход", form=form, message=response.get("message", "Error"))
        _user = User()
        _user.id_name = response["id_name"]
        _user.id = response["id"]
        _user.username = response["username"]
        _user.created_date = response["created_date"]
        login_user(_user, remember=form.remember_me.data)
        return redirect("/client_page")
    return render_template("login.html", title="Вход", form=form)
