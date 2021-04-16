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
            item_id = item['id']
            print(item_id)
            item['images'] = item_dao.item_image_list(item_id, connection)
            print(item)

            item['review'] = item_dao.count_avg_review(item_id, connection)
            print(item)


        return {'data' : item_list}