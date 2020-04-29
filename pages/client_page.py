from flask import render_template, Blueprint, redirect
from flask_login import current_user

client_page = Blueprint("client_page", __name__,
                      template_folder="templates")


@client_page.route("/client_page", methods=["GET", "POST"])
def page():
    if not current_user.is_authenticated:
        return redirect("/login")
    return render_template("client_page.html", name=current_user.username)
