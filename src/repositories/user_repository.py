from werkzeug.security import generate_password_hash, check_password_hash

from src.exceptions.user_not_found_error import UserNotFoundError
from src.models.user import User


class UserRepository:

    @staticmethod
    def create_user(username, email, password):
        hashed_password = generate_password_hash(password)
        user = User(
            username=username,
            email=email,
            password=hashed_password
        )
        user.save()
        return user

    @staticmethod
    def get_user_by_username(username):
        return User.objects(username=username).first()

    @staticmethod
    def get_user_by_email(email):
        return User.objects(email=email).first()

    @staticmethod
    def get_user_by_id(id_user):
        return User.objects(id=id_user).first()

    @staticmethod
    def authenticate_user(email, password):
        user = UserRepository.get_user_by_email(email)
        password_check = check_password_hash(user.password, password)
        if not password_check:
            raise UserNotFoundError(f'Incorrect username or password')
        return user