from flask import request, Blueprint, Flask, g

from service.reservation_service import ReservationService
from db_connector import connect_db
from response import *
from utils import login_decorator

class ReservationView():
    reservation_app = Blueprint('reservation_app', __name__, url_prefix='/reservation')

    @reservation_app.route('/<int:accommodation_id>', methods=['POST'])
    @login_decorator
    def reservation_progress(accommodation_id):
        """ User reservation 
        Author:    
            Binho Song
        Returns:
			result: SUCCESS
        """
        try: 
            connection = None
            data = request.json
            user_id = g.token_info['user_id']

            if 'start_date' not in data:
                raise ApiException(400, NOT_START_DATE)
            if 'end_date' not in data:
                raise ApiException(400, NOT_END_DATE)
            if 'total_price' not in data:
                raise ApiException(400, NOT_TOTAL_PRICE)
            if 'accommodation_price' not in data:
                raise ApiException(400,NOT_ACCOMMODATION_PRICE)
            if 'service_fee' not in data:
                raise ApiException(400,NOT_SERVICE_FEE)
            if 'cleaning_fee' not in data:
                raise ApiException(400,NOT_CLEANING_FEE)
            if 'total_adults' not in data:
                raise ApiException(400, NOT_TOTAL_ADULTS)

            reservation_info = {
                'accommodation_id' : accommodation_id,
                'user_id' : user_id,
                'start_date' : data['start_date'],
                'end_date' : data['end_date'],
                'total_price' : data['total_price'],
                'accommodation_price' : data['accommodation_price'],
                'service_fee' : data['service_fee'],
                'cleaning_fee' : data['cleaning_fee'],
                'total_adults' : data['total_adults'],
                'total_children' : data.get('total_children', 0),
                'total_infants' : data.get('total_infants', 0),
                'sales' : data.get('sales', 0.00)
            }
            connection = connect_db()
            reservation_service = ReservationService()
            reservation_service.reservation_progress_service(reservation_info, connection)
            connection.commit()

            return {"message" : "SUCCESS"}

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()