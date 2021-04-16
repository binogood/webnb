from flask import request, Blueprint, Flask

from service.item_service import ItemService
from db_connector import connect_db
from response import *
from datetime import datetime

class ItemView:
    item_app = Blueprint('item_app', __name__, url_prefix='/item')

    def __init__(self):
        pass

    @item_app.route('list', methods=['GET'])
    def item_list():
        """ 숙소 리스트
        Author: Binho Song
        Returns:
            숙소 리스트 
        """
        connection = None
        try:
            data = request.json

            if 'start_date' not in data:
                raise ApiException(400, INVALID_INPUT_START_DATE)
            if 'end_date' not in data:
                raise ApiException(400, INVALID_INPUT_END_DATE)

            item_filter = {
                'contury' : data.get('contury', None),
                'city' : data.get('city', 'San francisco'),
                'start_date' : data.get('start_date',None),
                'end_date' : data.get('end_date',None),
                'adults' : data.get('adults', None),
                'childens' : data.get('childens', None),
                'infants' : data.get('infants', None),
            }

            connection = connect_db()
            item_service = ItemService()
            item_list = item_service.item_list_service(item_filter, connection)
            return item_list
        
        except ApiException as e:
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()
    
    # @item_app.route('<int:accommodation_id>', methods=['GET'])
    # def detail_list_view():
    #     """ 숙소 디테일 뷰
    #     Author: Binho Song
    #     Returns:
    #         숙소 디테일 뷰
    #     """
    #     connection = None
    #     try: 
    #         data = request.json
    #         if 'accommodation_id' not in data:
    #             raise ApiException(400, NOT_ACCOMMODATEION_ID)

    #         item_id = {
    #             'accommodation_id' : data['accommodation_id'],
    #             'start_date' : data['start_date'],
    #             'end_date' : data['end_date']
    #         }