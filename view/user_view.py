from flask import request, Blueprint, Flask, g

from service.user_service import UserService
from db_connector import connect_db
from response import *
from utils import login_decorator

BASIC_USER = 1

class UserView:
    user_app = Blueprint('user_app', __name__, url_prefix='/user')

    @user_app.route('signup', methods=['POST'])
    def sign_up_user():
        """ User view
        Author:    
            Binho Song
        Returns:
			result: {"message": "USER_CREATED"}
        """
        connection = None
        try:   
            data = request.json
            if 'first_name' not in data:
                raise ApiException(400, INVALID_INPUT_FIRST_NAME)
            if 'last_name' not in data:
                raise ApiException(400, INVALID_INPUT_LAST_NAME)
            if 'password' not in data:    
                raise ApiException(400, INVALID_INPUT_PASSWORD)
            if 'date_of_birth' not in data:
                raise ApiException(400, INVALID_INPUT_DATE_OF_BIRTH)
            if 'phone_number' not in data:
                raise ApiException(400, INVALID_INPUT_PHONE_NUMBER)
            if 'email' not in data:
                raise ApiException(400, INVALID_INPUT_EMAIL)

            user_info = {
                'email' : data['email'],
                'first_name' : data['first_name'],
                'last_name' : data['last_name'],
                'password' : data['password'],
                'date_of_birth' : data['date_of_birth'],
                'phone_number' : data['phone_number'],
                'social_platform_id' : data.get('social_platform_id', BASIC_USER),
                'profile_photo_url' : data.get('profile_photo_url', None)
            }

            connection = connect_db()
            user_service = UserService()
            user_service.create_user_service(user_info, connection)
            connection.commit()

            return {"message": "USER_CREATED"}

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()
    
    @user_app.route('login', methods=['POST'])
    def login_user():
        """ User login view
        Author:    
            Binho Song
        Returns:
			result: user_login
        """
        connection = None
        try:
            data = request.json

            user_info = {
                'email' : data['email'],
                'password' : data['password']
            }

            connection = connect_db()
            user_service = UserService()
            user_login = user_service.login_user_service(user_info, connection)
            return user_login

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()

    @user_app.route('mypage/<int:mypage_status>', methods=['GET'])
    @login_decorator
    def user_mypage_view(mypage_status):
        """ User mypage view
        Author:    
            Binho Song
        Returns:
			result: mypage_list
        """
        connection = None
        try:
            user_id = g.token_info['user_id']

            mypage_info = {
                'user_id' : user_id,
                'mypage_status' : mypage_status
            }

            connection = connect_db()
            user_service = UserService()
            mypage_list = user_service.user_mypage_service(mypage_info, connection)

            return mypage_list

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e
        
        finally:
            if connection:
                connection.close()


