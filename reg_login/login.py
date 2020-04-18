from flask import Blueprint, redirect, render_template
from .forms import LoginForm
from data.user import User
from requests import get
from flask_login import login_user

login = Blueprint("login", __name__,
                  template_folder="templates")


@login.route("/login", methods=["GET", "POST"])
def login_func():
    form = LoginForm()
    if form.validate_on_submit():
        params = {
            "id_name": form.id_name.data,
            "password": form.password.data
        }
        response = get("http://localhost:8080/api/useracc", json=params).json()
        if not response.get("success", False):
            return render_template("login.html", title="Вход", form=form, message=response.get("message", "Error"))
        current_user = User()
        current_user.id_name = response["id_name"]
        current_user.id = response["id"]
        current_user.username = response["username"]
        current_user.created_date = response["created_date"]
        login_user(current_user, remember=form.remember_me.data)
        return redirect("/")
    return render_template("login.html", title="Вход", form=form)
