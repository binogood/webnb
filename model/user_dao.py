import pymysql

class UserDao:

    def find_user_dao(self, user_info, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    id,
                    email,
                    password,
                    is_delete
                FROM
                    users
                WHERE
                    email = %(email)s
            """
            cursor.execute(query, user_info)
        return cursor.fetchone()

    def user_identifier_dao(self, user_info, connection):
        """ 유저 식별
        Author: Binho Song
        Args:
            user_info (dict): 유저정보
            connection: 커넥션
        Returns:
            created_user: user_id
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    is_delete
                FROM 
                    users
                WHERE
                    id = %(user_id)s
            """
            cursor.execute(query, user_info)
        return cursor.fetchone()

    def exists_user_email_dao(self, user_info, connection):
        """ 유저 이메일 중복 확인
        Author: Binho Song
        Args:
            user_info (dict): 유저정보
            connection: 커넥션
        Returns:
            created_user: 중복 email의 id
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    email
                FROM
                    users
                WHERE
                    email = %(email)s
            """
            cursor.execute(query, user_info)
        return cursor.fetchone()

    def create_user_dao(self, user_info, connection):
        """ 유저 회원가입
        Author: Binho Song
        Args:
            user_info (dict): 유저정보
            connection: 커넥션
        Returns:
            created_user: 새로 회원가입한 유저 id
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO users (
                    first_name,
                    last_name,
                    password,
                    date_of_birth,
                    email,
                    profile_photo_url,
                    phone_number,
                    social_platform_id,
                    is_delete,
                    created_at
                )
                VALUES (
                    %(first_name)s,
                    %(last_name)s,
                    %(password)s,
                    %(date_of_birth)s,
                    %(email)s,
                    %(profile_photo_url)s,
                    %(phone_number)s,
                    %(social_platform_id)s,
                    0,
                    NOW()
                )
            """
            cursor.execute(query, user_info)
        return cursor.lastrowid

    def create_user_log_dao(self, user_info, connection):
        """ 유저 회원가입 로그
        Author: Binho Song
        Args:
            user_info (dict): 유저정보
            connection: 커넥션
        Returns:
            created_user: 새로 회원가입한 유저 id
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
               INSERT INTO users_log (
                   first_name,
                   last_name,
                   password,
                   date_of_birth,
                   email,
                   profile_photo_url,
                   phone_number,
                   social_platform_id,
                   is_delete,
                   created_at,
                   user_id,
                   changer_id,
                   change_date
               )
               VALUES (
                   %(first_name)s,
                   %(last_name)s,
                   %(password)s,
                   %(date_of_birth)s,
                   %(email)s,
                   %(profile_photo_url)s,
                   %(phone_number)s,
                   %(social_platform_id)s,
                   0,
                   NOW(),
                   %(user_id)s,
                   %(changer_id)s,
                   NOW()
               )
               """
            cursor.execute(query, user_info)
        return cursor.lastrowid