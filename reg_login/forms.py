from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    id_name = StringField("ID name", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Повторите пароль", validators=[DataRequired()])
    username = StringField("Имя пользователя", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироватьтся")


class LoginForm(FlaskForm):
    id_name = StringField("ID name", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомните меня")
    submit = SubmitField("Войти")
