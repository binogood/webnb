import pymysql

class ItemDao:
    def __init__(self):
        pass

    def find_item_dao(self, item_filter, connection):
        """ accommodation list
        Author: 
            Binho Song
        Args:    
			- item_filter : filter 
			- connection : connection
        Returns:
			result: accommodation list
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    a.id as accommodation_id,
                    a.max_capacity,
                    a.title,
                    a.price,
                    a.latitude,
                    a.longitude,
                    ac.name
                FROM
                    accommodations a
                JOIN
                    accommodation_amenities aa
                    ON a.id = aa.accommodation_id
                JOIN
                    amenities am
                    ON aa.amenity_id = am.id
                JOIN
                    accommodation_facilities af
                    ON a.id = af.accommodation_id
                JOIN
                    facilities f
                    ON af.facility_id = f.id
                JOIN
                    accommodation_categories ac
                    ON ac.id = a.accommodation_category_id
            """
            if item_filter['number_of_bathroom']:
                query += """
                    AND a.number_of_bathroom >= %(number_of_bathroom)s
                """
            if item_filter['number_of_bedroom']:
                query += """
                    AND a.number_of_bedroom >= %(number_of_bedroom)s
                """
            if item_filter['number_of_bed']:
                query += """
                    AND a.number_of_bed >= %(number_of_bed)s
                """
            if item_filter['place']:
                query += """
                    AND ac.name in (%(place)s)
                """
            if item_filter['amenity']:
                query += """
                    AND am.name in (%(amenity)s)
                """
            if item_filter['facility']:
                query += """
                    AND af.facility_id in (%(facility)s)
                """
            if item_filter['amenity'] or item_filter['facility'] or item_filter['place']:
                query += """
                    GROUP BY a.id
                    HAVING count(a.id) = %(filter_len)s
                """
            else:
                query += """
                    WHERE
                        a.city = %(city)s
                        AND a.max_capacity >= %(max_capacity)s
                    GROUP BY
                        a.id
                    ORDER BY
                        a.id
                """
            cursor.execute(query, item_filter)
        return cursor.fetchall()
    
    def item_image_list_dao(self, accommodation_id, connection):
        """ accommodation image list
        Author: 
            Binho Song
        Args:    
			- item_filter : accommodation_id 
			- connection : connection
        Returns:
			result: accommodation image list
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    image_url
                FROM 
                    accommodation_images
                WHERE
                    accommodation_id = %(accommodation_id)s
            """
            cursor.execute(query, {'accommodation_id':accommodation_id})
            # cursor.execute(query, accommodation_id)
        return cursor.fetchall()

    def count_avg_review_dao(self,accommodation_id, connection):
        """ accommodation review list
        Author: 
            Binho Song
        Args:    
			- item_filter : accommodation_id 
			- connection : connection
        Returns:
			result: accommodation review list
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    ROUND(AVG(accommodation_rate),1) as review_avg,
                    COUNT(*) as review_count
                FROM
                    reviews
                WHERE
                    accommodation_id = %(accommodation_id)s
            """
            cursor.execute(query, {'accommodation_id':accommodation_id})
            # cursor.execute(query, accommodation_id)
        return cursor.fetchone()

    def item_detail_view_dao(self, item_info, connection):
        """ accommodation detail view
        Author: 
            Binho Song
        Args:    
			- item_filter : accommodation_id 
			- connection : connection
        Returns:
			result: accommodation detail view
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    a.title,
                    a.country,
                    a.city,
                    a.latitude,
                    a.longitude,
                    a.max_capacity,
                    a.price,
                    a.cleaning_fee,
                    a.number_of_bed,
                    a.number_of_bedroom,
                    a.number_of_bathroom,
                    a.location_content,
                    u.last_name
                FROM
                    accommodations a
                INNER JOIN
                    users u
                    ON u.id = a.user_id
                WHERE
                    a.id = %(accommodation_id)s
            """
            cursor.execute(query, item_info)
        return cursor.fetchone()
    
    def item_detail_view_amenitie_dao(self, item_info, connection):
        """ Accommodation amenities list
        Author: 
            Binho Song
        Args:    
			- item_filter : accommodation_id 
			- connection : 커넥션
        Returns:
			result: Accommodation amenities list
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    am.name,
                    am.icon
                FROM
                    accommodation_amenities aa
                INNER JOIN
                    amenities am
                    on am.id = aa.amenity_id
                WHERE
                    accommodation_id = %(accommodation_id)s     
            """
            cursor.execute(query, item_info)
        return cursor.fetchall()
    
    def item_detail_view_review_dao(self, item_info, connection):
        """ Accommodation review list
        Author: 
            Binho Song
        Args:    
			- item_filter : accommodation_id 
			- connection : connection
        Returns:
			result: Accommodation review list
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    r.content,
                    r.accommodation_rate,
                    r.created_at,
                    u.last_name
                FROM
                    reviews r
                INNER JOIN
                    users u
                    ON u.id = r.user_id
                WHERE
                    r.accommodation_id = %(accommodation_id)s
            """
            cursor.execute(query, item_info)
        return cursor.fetchall()

    def item_detail_image_dao(self, item_info, connection):
        """ Accommodation image list
        Author: 
            Binho Song
        Args:    
			- item_filter : accommodation_id 
			- connection : connection
        Returns:
			result: Accommodation image list
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    image_url
                FROM 
                    accommodation_images
                WHERE
                    accommodation_id = %(accommodation_id)s
            """
            cursor.execute(query, item_info)
        return cursor.fetchall()


    def detail_count_avg_review_dao(self,item_info, connection):
        """ Accommodation review count and average
        Author: 
            Binho Song
        Args:    
			- item_filter : accommodation_id 
			- connection : connection
        Returns:
			result: Accommodation review count and average
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    ROUND(AVG(accommodation_rate),1) as review_avg,
                    COUNT(*) as review_count
                FROM
                    reviews
                WHERE
                    accommodation_id = %(accommodation_id)s
            """
            cursor.execute(query, item_info)
        return cursor.fetchone()

    
    def accommodation_like_add_dao(self, wish, connection):
        """ User wishlist add
        Author: 
            Binho Song
        Args:    
			- item_filter : accommodation_id, user_id
			- connection : connection
        Returns:
			result: User wishlist add
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO accommodation_wishlist(
                    user_id,
                    accommodation_id
                ) VALUES (
                    %(user_id)s,
                    %(accommodation_id)s
                )
            """
            cursor.execute(query, wish)
        return cursor.lastrowid

    def accommodation_like_delete_dao(self, wish, connection):
        """ User wishlist delete
        Author: 
            Binho Song
        Args:    
			- item_filter : accommodation_id, user_id
			- connection : connection
        Returns:
			result: User wishlist delete
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                DELETE FROM
                    accommodation_wishlist
                WHERE
                    user_id = %(user_id)s
                    AND accommodation_id = %(accommodation_id)s
            """
            cursor.execute(query, wish)
        return True

    def accommodation_like_check_list_dao(self, wish, connection):
        """ User wishlist check
        Author: 
            Binho Song
        Args:    
			- item_filter : accommodation_id, user_id
			- connection : connection
        Returns:
			result: User wishlist check
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    accommodation_id
                FROM
                    accommodation_wishlist
                WHERE
                    user_id = %(user_id)s
                    AND accommodation_id = %(accommodation_id)s
            """
            cursor.execute(query, wish)
        return cursor.fetchone()
    
    def user_wishlist_all_dao(self, wishlist_info, connection):
        """ User wishlist all
        Author: 
            Binho Song
        Args:    
			- item_filter : user_id
			- connection : connection
        Returns:
			result: User wishlist all
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
               SELECT
                    aw.accommodation_id,
                    ai.image_url,
                    a.city,
                    a.title,
                    a.price
                FROM
                    accommodation_wishlist aw
                INNER JOIN
                    accommodations a
                    ON a.id = aw.accommodation_id
                INNER JOIN
                    accommodation_images ai
                    ON ai.accommodation_id = a.id
                WHERE
                    aw.user_id = %(user_id)s
                GROUP BY
	                aw.accommodation_id
            """
            cursor.execute(query, wishlist_info)
        return cursor.fetchall()