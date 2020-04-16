from flask import Blueprint, redirect, render_template
from .forms import LoginForm
from data import db_session
from data.user import User
from flask_login import login_user

login = Blueprint("login", __name__,
                  template_folder="templates")


@login.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()

        session.close()
