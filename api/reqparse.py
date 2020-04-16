from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument("idname", required=True)
parser.add_argument("password", required=True)
parser.add_argument("username", required=True)
