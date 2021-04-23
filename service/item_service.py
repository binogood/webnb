from model.item_dao import ItemDao
from flask import jsonify
from response import *


class ItemService:
    def __init__(self):
        pass

    def item_list_service(self, item_filter, connection):
        """ Item list service
        Author: 
            Binho Song
        Args:    
			- item_filter : ifem_filter
			- connection : connection
        Returns:
			result: item_list
        """
        item_dao = ItemDao()
        item_list = item_dao.find_item_dao(item_filter, connection)

        for item in item_list:
            accommodation_id = item['accommodation_id']
            wish = {
                'accommodation_id' : accommodation_id,
                'user_id' : item_filter['user_id']
            }
            item['images'] = item_dao.item_image_list_dao(accommodation_id, connection)
            item['review'] = item_dao.count_avg_review_dao(accommodation_id, connection)
            item['wishlist'] = item_dao.accommodation_like_check_list_dao(wish, connection)


        return {'data' : item_list}

    def item_detail_view_service(self, item_info, connection):
        """ Item detail view service 
        Author: 
            Binho Song
        Args:    
			- item_filter : item_info
			- connection : connection
        Returns:
			result: item_detail_view
        """
        item_dao = ItemDao()
        item_detail_view = item_dao.item_detail_view_dao(item_info, connection)
        item_detail_view['images'] = item_dao.item_detail_image_dao(item_info, connection)
        item_detail_view['amenities'] = item_dao.item_detail_view_amenitie_dao(item_info,connection)
        item_detail_view['review'] = item_dao.item_detail_view_review_dao(item_info, connection)
        item_detail_view['review_avg'] = item_dao.detail_count_avg_review_dao(item_info, connection)

        return {'data' : item_detail_view}
        

    def accommodation_like_add_service(self, wish, connection):
        """ User accommodation wishlist add
        Author: 
            Binho Song
        Args:    
			- item_filter : wish
			- connection : connection
        Returns:
			result: wishlist
        """
        item_dao = ItemDao()
        wishlist = item_dao.accommodation_like_check_list_dao(wish, connection)
        if wishlist:
            wishlist = item_dao.accommodation_like_delete_dao(wish, connection)
        else:
            wishlist = item_dao.accommodation_like_add_dao(wish, connection)

        return wishlist

    # def accommodation_like_all_list_service(self, wish, connection):
    #     """ 좋아요 리스트
    #     Author: Binho Song
    #     Args:
    #         wish : 유저가 선택한 숙소 정보
    #         connection: 커넥션
    #     Returns:
    #         좋아요 리스트
    #     """
    #     item_dao = ItemDao()
    #     wishlist = item_dao.accommodation_all_like_list_dao(wish, connection)

    def user_wishlist_all_service(self, wishlist_info, connection):
        """ User accommodation wishlist
        Author: 
            Binho Song
        Args:    
			- item_filter : wishlist_info
			- connection : connection
        Returns:
			result: wishlist
        """

        item_dao = ItemDao()

        wishlist = item_dao.user_wishlist_all_dao(wishlist_info, connection)

        for item in wishlist:
            accommodation_id = item['accommodation_id']
            item['review'] = item_dao.count_avg_review_dao(accommodation_id, connection)

        return wishlist