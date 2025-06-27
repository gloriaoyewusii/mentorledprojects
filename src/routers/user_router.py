import os
from datetime import timedelta

from flask import Blueprint, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager

from controllers.usercontroller import UserController
from src.services.user_service import UserService

user_router = Blueprint('user_router', __name__)
user_service = UserService()
user_controller = UserController(user_service)

@user_router.route('/register', methods=['POST'])
def register_user():
    return user_controller.register()


@user_router.route('/login', methods=['POST'])
def login_user():
    return user_controller.login()

@user_router.route('/view-profile', methods=['GET'])
def view_profile():
    return user_controller.view_profile()

@user_router.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return make_response(jsonify(logged_in_as=current_user), 200)

