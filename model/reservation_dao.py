import pymysql

class ReservationDao():
    def __init__(self):
        pass

    def reservation_progress_dao(self, reservation_info, connection):
        """ reservation 
        Author: 
            Binho Song
        Args:    
			- item_filter : reservation_info
			- connection : connection
        Returns:
			result: reservation
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
                INSERT INTO reservations (
                    accommodation_id,
                    user_id,
                    start_date,
                    end_date,
                    total_price,
                    accommodation_price,
                    service_fee,
                    cleaning_fee,
                    total_adults,
                    total_children,
                    total_infants,
                    sales,
                    reservation_status_id,
                    created_at
                ) VALUES (
                    %(accommodation_id)s,
                    %(user_id)s,
                    %(start_date)s,
                    %(end_date)s,
                    %(total_price)s,
                    %(accommodation_price)s,
                    %(service_fee)s,
                    %(cleaning_fee)s,
                    %(total_adults)s,
                    %(total_children)s,
                    %(total_infants)s,
                    %(sales)s,
                    2,
                    NOW()
                )
            """
            cursor.execute(query, reservation_info)
        return cursor.fetchone()

    # def reservation_progress_dao(self, reservation_info, connection):
    #     with connection.cursor(pymysql.cursors.DictCursor) as cursor:
    #         query = """
    #             INSERT INTO reservations_log(
    #                 reservation_id,
    #                 accommodation_id,
    #                 user_id,
    #                 start_date,
    #                 end_date,
    #                 total_price,
    #                 accommodation_price,
    #                 service_fee,
    #                 cleaning_fee,
    #                 total_adults,
    #                 total_children,
    #                 total_infants,
    #                 sales,
    #                 reservation_status_id,
    #                 created_at,
    #                 changer_id,
    #                 change_date
    #             ) SELECT
    #                 r.reservation_id,
    #                 r.accommodation_id,
    #                 r.user_id,
    #                 r.start_date,
    #                 r.end_date,
    #                 r.total_price,
    #                 r.accommodation_price,
    #                 r.service_fee,
    #                 r.cleaning_fee,
    #                 r.total_adultss,
    #                 r.total_children,
    #                 r.total_infants,
    #                 r.sales,
    #                 r.reservation_status_id,
    #                 r.created_at,
    #                 %(user_id)s,
    #                 NOW()
    #             FROM
    #                 reservations_log r
    #             WHERE
    #                 r.id = %(reservation_id)s

    #         """
    #         cursor.execute(query, reservation_info)
    #     return cursor.fetchone()