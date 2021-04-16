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
                    a.id,
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
    
    def item_image_list(self, item_id, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    image_url
                FROM 
                    accommodation_images
                WHERE
                    accommodation_id = %(item_id)s
            """
            cursor.execute(query, {'item_id':item_id})
        return cursor.fetchall()

    def count_avg_review(self,item_id, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                SELECT
                    ROUND(AVG(accommodation_rate),1) as review_avg,
                    COUNT(*) as review_count
                FROM
                    reviews
                WHERE
                    accommodation_id = %(item_id)s
            """
            cursor.execute(query, {'item_id':item_id})
        return cursor.fetchone()