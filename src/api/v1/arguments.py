from __future__ import annotations

from flask_restful import reqparse


def create_parser_args_signup():
    sign_up_parser = reqparse.RequestParser()
    common_argument = {"location": "form", "type": str}
    sign_up_parser.add_argument(
        "login",
        **common_argument,
        required=True,
        help="Login required",
    )
    sign_up_parser.add_argument(
        "password",
        **common_argument,
        required=True,
        help="Password required",
    )
    sign_up_parser.add_argument(
        "email",
        **common_argument,
        required=True,
        help="Email required",
    )
    sign_up_parser.add_argument(
        "first_name",
        **common_argument,
        required=False,
    )
    sign_up_parser.add_argument(
        "User-Agent",
        dest="user_agent",
        location="headers",
    )
    return sign_up_parser.parse_args()


def create_parser_args_login():
    common_argument = {"location": "form", "type": str}
    login_parser = reqparse.RequestParser()
    login_parser.add_argument(
        "login",
        **common_argument,
        required=True,
        help="Login required",
    )
    login_parser.add_argument(
        "password",
        **common_argument,
        required=True,
        help="Password required",
    )
    login_parser.add_argument(
        "User-Agent",
        dest="user_agent",
        location="headers",
    )
    return login_parser.parse_args()


def create_parser_args_change_auth_data():
    common_argument = {"location": "form", "type": str, "required": False}
    auth_change_parser = reqparse.RequestParser()
    auth_change_parser.add_argument(
        "login",
        **common_argument,
        help="Login required to change",
    )
    auth_change_parser.add_argument(
        "password",
        **common_argument,
        help="Password required to change",
    )
    return auth_change_parser.parse_args()
