from flask import request, Blueprint, Flask, g

from service.item_service import ItemService
from db_connector import connect_db
from response import *
from datetime import datetime, date
from utils import login_decorator

NOW = date.today()
TODAY = NOW.isoformat()

class ItemView:
    item_app = Blueprint('item_app', __name__, url_prefix='/item')

    def __init__(self):
        pass

    @item_app.route('/list', methods=['POST'])
    @login_decorator
    def item_list():
        """ Item list view
        Author:    
            Binho Song
        Returns:
			result: item_list
        """
        connection = None
        try:
            data = request.json
            user_id = g.token_info['user_id']

            amenity_len = len(request.values.getlist('amenity'))
            place_len = len(request.values.getlist('place'))
            facility_len = len(request.values.getlist('facility'))
            amenity = str(request.values.getlist('amenity', None))[1:-1]
            place = str(request.values.getlist('place', None))[1:-1]
            facility = str(request.values.getlist('facility', None))[1:-1]

            if amenity_len == 0: 
                amenity_len = 1

            if facility_len == 0: 
                facility_len = 1

            if place_len == 0: 
                place_len = 1 

            max_capacity = data.get('adults', 0) + data.get('children', 0) + data.get('infants', 0)
            
            item_filter = {
                'user_id' : user_id,
                'contury' : data.get('contury', None),
                'city' : data.get('city', 'San francisco'),
                'start_date' : data.get('start_date',TODAY),
                'end_date' : data.get('end_date',None),
                'max_capacity' : max_capacity,
                'number_of_bathroom' : data.get('number_of_bathroom', None),
                'number_of_bedroom' : data.get('number_of_bedroom', None),
                'number_of_bed' : data.get('number_of_bed', None),
                'place' : place,
                'facility' : facility,
                # 'amenity' : amenity,
                'amenity' :request.values.get('amenity', None)
            }

            item_filter['filter_len'] = amenity_len * facility_len * place_len

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
    
    @item_app.route('/<int:accommodation_id>', methods=['POST'])
    def detail_list_view(accommodation_id):
        """ Item detail view
        Author:    
            Binho Song
        Returns:
			result: item_detail_view
        """
        connection = None
        try: 
            data = request.json
            # if 'accommodation_id' not in data:
            #     raise ApiException(400, NOT_ACCOMMODATEION_ID)

            item_info = {
                'accommodation_id' : accommodation_id,
            }

            connection = connect_db()
            item_service = ItemService()
            item_detail_view = item_service.item_detail_view_service(item_info, connection)

            return item_detail_view

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()

    @item_app.route('/like/<int:accommodation_id>', methods=['POST'])
    @login_decorator
    def accommodation_like_add(accommodation_id):
        """ User accommodation wishlist add
        Author:    
            Binho Song
        Returns:
			result: SUCCESS
        """
        connection = None
        try:
            data = request.json
            user_id = g.token_info['user_id']
            wish = {
                'user_id' : user_id,
                'accommodation_id' : accommodation_id
            }
            connection = connect_db()
            item_service = ItemService()
            wishlist = item_service.accommodation_like_add_service(wish, connection)
            connection.commit()

            return {"message" : "SUCCESS"}

        except ApiException as e:
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()

    @item_app.route('/wishlist', methods=['GET'])
    @login_decorator
    def user_wishlist_view():
        """ User wishlist view
        Author:    
            Binho Song
        Returns:
			result: wishlist
        """
        connection = None
        try:
            user_id = g.token_info['user_id']
            wishlist_info = {
                'user_id' : user_id
            }
            connection = connect_db()
            item_service = ItemService()
            wishlist = item_service.user_wishlist_all_service(wishlist_info, connection)

            return {'data' : wishlist}
        
        except ApiException as e:
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()