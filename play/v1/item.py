from __future__ import absolute_import, division, print_function

from flask_restful import Resource, marshal_with, marshal, request

from utils import model
from main import api_v1


class Item(model.Model):
    value = model.ndb.StringProperty()
    created = model.ndb.DateTimeProperty(auto_now_add=True)
    modified = model.ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def fields(cls, endpoint='api.item'):
        return super(Item, cls).fields(endpoint=endpoint)

    @classmethod
    def query(cls, *args, **kwargs):
        return super(Item, cls).query(*args, **kwargs).order(-cls.created)


@api_v1.resource('/item/', '/item/<string:key>', endpoint='api.item')
class ItemEndpoint(Resource):
    def get(self, key=None):
        if key is None:
            return self.get_all()
        else:
            return self.get_one(key)

    @marshal_with(Item.fields())
    def post(self):
        data = request.get_json(force=True)

        item = Item()
        item.value = data['value']
        item.put()

        return item, 201

    @marshal_with(Item.fields())
    def put(self, key):
        data = request.get_json(force=True)

        item = Item.get_by_key(key)
        item.value = data['value']
        item.put()

        return item, 200

    def delete(self, item_id):
        pass

    def get_all(self):
        results, next_cursor, more = Item.fetch_page(count=10, cursor=request.args.get('cursor'))

        return {
            'next_cursor': next_cursor.urlsafe(),
            'more': more,
            'items': marshal(results, Item.fields())
        }

    @marshal_with(Item.fields())
    def get_one(self, key):
        item = Item.get_by_key(key)
        if not item:
            return {'error': 'Item not found.'}, 404
        return item
