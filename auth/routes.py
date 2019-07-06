from flask_restful import Resource
from flask import session
from auth.parsers import auth_parser

user = dict()


class Login(Resource):
    def post(self):
        pass


class Logout(Resource):
    def get(self):
        pass


class Registration(Resource):
    def post(self):
        pass
