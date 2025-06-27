import datetime
import os

import jwt
from flask import request, make_response, jsonify


from src.dtos.request.registrationrequest import RegistrationRequest
from src.exceptions.RegistrationFailedError import RegistrationFailedError
from src.exceptions.existing_user_error import ExistingUserError
from src.exceptions.user_not_found_error import UserNotFoundError
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')


class UserController:
    def __init__(self, user_service : UserService):
        self.user_service = user_service

    @staticmethod
    def register():
        user_data = request.get_json()
        user_name = user_data.get('username')
        user_password = user_data.get('password')
        user_email = user_data.get('email')

        existing_user = UserRepository.get_user_by_email(user_email)
        if existing_user:
            return jsonify({'message': 'User already exists'}), 409

        try:
            UserService.register_user(user_name, user_email, user_password)
            user = User.objects.get(email=user_email)

            user_request = RegistrationRequest()
            serialised_user = user_request.dump(user)
            return make_response(jsonify({
                "message": "User registered successfully",
                "user": serialised_user}), 201)

        except RegistrationFailedError as e:
            return make_response(jsonify({"error": str(e)}), 401)
        except ExistingUserError as e:
            return make_response(jsonify({"error": str(e)}), 401)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 401)

    @staticmethod
    def login():
        user_data = request.get_json()

        user_password = user_data.get('password')
        user_email = user_data.get('email')

        if not user_email or not user_password:
            return make_response(jsonify({"error": "Email address and password are required"}), 400)
        try:
            user_details = UserService.login_user(user_email, user_password)
            payload = {
                "user":{
                    "username": user_details.username,
                    "email": user_details.email,
                    },
                "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
                }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return make_response(jsonify({
                "message": "User login successfully",
                "user":{
                    "username": user_details.username,
                    "email": user_details.email,
                    },
                "token": token
            }), 200)
        except UserNotFoundError as e:
            return make_response(jsonify({"error": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 401)


    @staticmethod
    def view_profile():
        user_data = request.get_json()
        user_email = user_data.get('email')
        if not user_email:
            return make_response(jsonify({"error": "Email address is required"}), 400)

        try:
            user_details = UserService.view_profile(user_email)
            return make_response(jsonify({"User profile":user_details}), 200)
        except UserNotFoundError as e:
            return make_response(jsonify({"error": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 401)






