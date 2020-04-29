from flask_restful import reqparse


# parser for register & login
reg_login_parser = reqparse.RequestParser()
reg_login_parser.add_argument("id_name", required=True)
reg_login_parser.add_argument("password", required=True)
reg_login_parser.add_argument("username")
# parser for another
table_parser = reqparse.RequestParser()
table_parser.add_argument("id_name", required=True)
table_parser.add_argument("user_token", required=True)
