from model.user_dao import UserDao
from flask import jsonify
import bcrypt
import jwt
from response import *
from config import SECRET_KEY, ALGORITHM

class UserService:
    def __init__(self):
        pass

    def create_user_service(self, user_info, connection):
        """ 유저 회원가입
        Author: Binho Song
        Args:
            user_info (dict): 유저정보
            connection: 커넥션
        Returns:
            created_user: 새로 회원가입한 유저 id
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
        """ 유저 로그인
        Author: Binho Song
        Args:
            user_info (dict): 유저정보
            connection: 커넥션
        Returns:
             jsonify({'accessToken': token, 'userId': user_id}), 201
             (유저 토큰이랑 user_id 반환해준다)
        """
        user_dao = UserDao()
        user = user_dao.find_user_dao(user_info, connection)
        print(user)
        print(user['password'])
        if user:
            if bcrypt.checkpw(user_info['password'].encode('utf-8'), user['password'].encode('utf-8')):
                token = jwt.encode({'user_id':user['id']}, SECRET_KEY, ALGORITHM)
                user_id = user['id']
                return jsonify({'accessToken':token, 'user_id':user_id}), 201
            if user['is_delete'] == 1:
                raise ApiException(400, USER_NOT_FOUND)    
            raise ApiException(400, PASSWORD_MISMATCH)
        raise ApiException(400, USER_NOT_FOUND)