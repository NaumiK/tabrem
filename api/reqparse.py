from flask_restful import reqparse


# parser for register & login
reg_login_parser = reqparse.RequestParser()
reg_login_parser.add_argument("id_name", required=True)
reg_login_parser.add_argument("password", required=True)
reg_login_parser.add_argument("username")
# parser for table
table_parser = reqparse.RequestParser()
table_parser.add_argument("name")
table_parser.add_argument("id")
table_parser.add_argument("description")
table_parser.add_argument("user_token", required=True)
# parser for status
status_parser = reqparse.RequestParser()
status_parser.add_argument("user_token", required=True)
status_parser.add_argument("name")
status_parser.add_argument("order")
status_parser.add_argument("id")
# parser for task
task_parser = reqparse.RequestParser()
task_parser.add_argument("user_token", required=True)
task_parser.add_argument("id")
task_parser.add_argument("name")
task_parser.add_argument("description")
