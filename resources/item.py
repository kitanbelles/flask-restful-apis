from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.items import ItemModel

items = []
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=int,
                        required=True,
                        help='Every item needs a store id')
    parser.add_argument('store_id',
                        type=float,
                        required=True,
                        help='every item needs a store')
    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"Message": "An error occurred"}
        if item:
            return item.json()
        return {"message": "item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"Message": "an item with that name, {} already exists".format(name)}, 400
        body = Item.parser.parse_args()
        item = ItemModel(name, body["price"], body["store_id"])
        try:
            item.save_to_db()
        except:
            return {"Message": "An error occurred while inserting the item"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"Message": "item deleted"}
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data["price"], data["store_id"])
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
