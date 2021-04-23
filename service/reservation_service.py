from model.reservation_dao import ReservationDao
from flask import jsonify
from response import *

class ReservationService:
    def __init__(self):
        pass

    def reservation_progress_service(self, reservation_info, connection):
        """ User reservation 
        Author: 
            Binho Song
        Args:    
			- item_filter : reservation_info
			- connection : connection
        Returns:
			result: True
        """
        reservation_dao = ReservationDao()
        reservation_id = reservation_dao.reservation_progress_dao(reservation_info, connection)
        # reservation_info = {'reservation_id' : reservation_id}
        # reservation_dao.reservation_progress_log_dao(reservation_info, connection)

        return True