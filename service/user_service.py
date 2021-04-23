from model.user_dao import UserDao
from flask import jsonify
import bcrypt
import jwt
from response import *
from config import SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta, date
import datetime

NOW = datetime.datetime.now()

class UserService:
    def __init__(self):
        pass

    def create_user_service(self, user_info, connection):
        """ User create service 
        Author: 
            Binho Song
        Args:    
			- item_filter : user_info
			- connection : connection
        Returns:
			result: user_info_id
        """
        user_dao = UserDao()
        email_exists = user_dao.exists_user_email_dao(user_info, connection)
        if email_exists:
            raise ApiException(400, DUPLICATED_EMAIL)

        hashed_password = bcrypt.hashpw(user_info['password'].encode('utf-8'),bcrypt.gensalt())
        user_info['password'] = hashed_password
        user_info_id = user_dao.create_user_dao(user_info, connection)
        user_info['user_id'] = user_info_id
        user_info['changer_id'] = user_info_id 
        user_dao.create_user_log_dao(user_info, connection)

        return user_info_id

    def login_user_service(self, user_info, connection):
        """ User login service
        Author: 
            Binho Song
        Args:    
			- item_filter : user_info
			- connection : connection
        Returns:
			result: token, user_id 
        """
        user_dao = UserDao()
        user = user_dao.find_user_dao(user_info, connection)

        if user:
            if bcrypt.checkpw(user_info['password'].encode('utf-8'), user['password'].encode('utf-8')):
                token = jwt.encode({'user_id':user['id']}, SECRET_KEY, ALGORITHM)
                user_id = user['id']
                return jsonify({'accessToken':token, 'user_id':user_id}), 201
            if user['is_delete'] == 1:
                raise ApiException(400, USER_NOT_FOUND)    
            raise ApiException(400, PASSWORD_MISMATCH)
        raise ApiException(400, USER_NOT_FOUND)

    def user_mypage_service(self, mypage_info, connection):
        """ User mypage list
        Author: 
            Binho Song
        Args:    
			- item_filter : mypage_info
			- connection : connection
        Returns:
			result: trip_list
        """
        user_dao = UserDao()
        mypage_list = user_dao.user_mypage_list_dao(mypage_info, connection)
        if mypage_info['mypage_status'] == 1:
            trip_list = [item for item in mypage_list if item['end_date'] > NOW]
        else :
            trip_list = [item for item in mypage_list if item['end_date'] < NOW]

        return {'data' : trip_list}

 
        

    