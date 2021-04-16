import pymysql

class ItemDao:
    def __init__(self):
        pass

    def find_item_dao(self, item_filter, connection):
        """ 숙소 리스트 ()
        Author: 
            Binho Song
        Args:    
			- item_filter : filter 값
			- connection : 커넥션
        Returns:
			result: 
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    a.id as accommodations_id,
                    a.max_capacity,
                    a.title,
                    a.price,
                    a.latitude,
                    a.longitude,
                    ac.name as accommodation_category
                FROM
                    accommodations a
                INNER JOIN
                    accommodation_categories ac
                    ON ac.id = a.accommodation_category_id
                WHERE
                    city = %(city)s
            """
            cursor.execute(query, item_filter)
        return cursor.fetchall()
    
    def item_image_list_dao(self, accommodation_id, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    image_url
                FROM 
                    accommodation_images
                WHERE
                    accommodation_id = %(accommodation_id)s
            """
            # cursor.execute(query, {'accommodation_id':accommodation_id})
            cursor.execute(query, accommodation_id)
        return cursor.fetchall()

    def count_avg_review_dao(self,accommodation_id, connection):
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
            cursor.execute(query, accommodation_id)
        return cursor.fetchone()

    def item_detail_view_dao(self, item_info, connection):
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
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    am.name
                FROM
                    accommodation_amenities aa
                INNER JOIN
                    amenities am
                    on am.id = aa.amenitie_id
                WHERE
                    accommodation_id = %(accommodation_id)s
                    
            """
            cursor.execute(query, item_info)
        return cursor.fetchall()
    
    def item_detail_view_review_dao(self, item_info, connection):
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