from model.item_dao import ItemDao
from flask import jsonify
from response import *


class ItemService:
    def __init__(self):
        pass

    def item_list_service(self, item_filter, connection):
        """ 숙소 리스트 출력
        Author: Binho Song
        Args:
            item_filter : 유저가 검색한 조건
            connection: 커넥션
        Returns:
             숙소 리스트 반환
        """
        item_dao = ItemDao()
        item_list = item_dao.find_item_dao(item_filter, connection)

        for item in item_list:
            accommodation_id = item['id']
            item['images'] = item_dao.item_image_list_dao(accommodation_id, connection)
            item['review'] = item_dao.count_avg_review_dao(accommodation_id, connection)

        return {'data' : item_list}

    def item_detail_view_service(self, item_info, connection):
        """ 숙소 디테일 뷰 
        Author: Binho Song
        Args:
            item_info : 유저가 선택한 숙소 정보
            connection: 커넥션
        Returns:
             숙소 정보 반환
        """
        item_dao = ItemDao()
        item_detail_view = item_dao.item_detail_view_dao(item_info, connection)
        item_detail_view['images'] = item_dao.item_image_list_dao(item_info, connection)
        item_detail_view['amenities'] = item_dao.item_detail_view_amenitie_dao(item_info,connection)
        item_detail_view['review'] = item_dao.item_detail_view_review_dao(item_info, connection)
        item_detail_view['review_avg'] = item_dao.count_avg_review_dao(item_info, connection)

        return {'data' : item_detail_view}
        