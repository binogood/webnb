import pymysql

class UserDao:

    def find_user_dao(self, user_info, connection):
        """ User check
        Author: 
            Binho Song
        Args:    
			- item_filter : user_email
			- connection : connection
        Returns:
			result: user_id 
        """
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
        """ User identifier
        Author: 
            Binho Song
        Args:    
			- item_filter : user_id
			- connection : connection
        Returns:
			result: user_id 
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
        """ User email exists
        Author: 
            Binho Song
        Args:    
			- item_filter : email
			- connection : connection
        Returns:
			result: user_id
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
        """ Create user
        Author: 
            Binho Song
        Args:    
			- item_filter : user_info
			- connection : connection
        Returns:
			result: user_id
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
        """ Create User log
        Author: 
            Binho Song
        Args:    
			- item_filter : user_info
			- connection : connection
        Returns:
			result: log_id 
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
               ) VALUES (
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

    def user_mypage_list_dao(self, mypage_info, connection):
        """ User mypage list
        Author: 
            Binho Song
        Args:    
			- item_filter : user_id
			- connection : connection
        Returns:
			result: User mypage list
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT DISTINCT
                    a.id as accommodation_id,
                    a.title,
                    a.city,
                    r.start_date,
                    r.end_date,
                    ai.image_url
                FROM 
                    reservations r
                INNER JOIN
                    accommodations a
                    ON a.id = r.accommodation_id
                INNER JOIN
                    accommodation_images ai
                    ON ai.accommodation_id = a.id
                WHERE
                    r.user_id = %(user_id)s
                GROUP BY
                    r.start_date
                ORDER BY
                    r.created_at
            """
            cursor.execute(query, mypage_info)
        return cursor.fetchall()


