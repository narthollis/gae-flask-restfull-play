from __future__ import absolute_import, division, print_function
import math
from flask import url_for

from flask_restful import Resource, marshal_with, marshal, request

from utils import model
from main import api_v1


class Item(model.Model):
    value = model.ndb.StringProperty()
    created = model.ndb.DateTimeProperty(auto_now_add=True)
    modified = model.ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def _get_kind(cls):
        return 'Item'

    @classmethod
    def fields(cls, endpoint='api.item'):
        return super(Item, cls).fields(endpoint=endpoint)

    @classmethod
    def query(cls, *args, **kwargs):
        return super(Item, cls).query(*args, **kwargs).order(-cls.created)


@api_v1.resource('/item/', '/item/<int:id>', endpoint='api.item')
class ItemEndpoint(Resource):
    def get(self, id=None):
        if id is None:
            return self.get_all()
        else:
            return self.get_one(id)

    @marshal_with(Item.fields())
    def post(self):
        data = request.get_json(force=True)

        item = Item()
        item.value = data['value']
        item.put()

        return item, 201

    @marshal_with(Item.fields())
    def put(self, id):
        data = request.get_json(force=True)

        item = Item.get_by_id(id)
        item.value = data['value']
        item.put()

        return item, 200

    def delete(self, id):
        pass

    def get_all(self):
        page_size = 10

        results, next_cursor, more, total = Item.fetch_page(page_size=page_size, cursor=request.args.get('cursor'))
        next_cursor = next_cursor.urlsafe()

        ret = {
            'totalCount': total,
            'pageCount': int(math.ceil(total / page_size)),
            'items': marshal(results, Item.fields())
        }
        if more:
            ret['next'] = {
                'href': url_for('api.item') + '?cursor=' + next_cursor,
            }

        return ret

    @marshal_with(Item.fields())
    def get_one(self, id):
        item = Item.get_by_id(id)
        if not item:
            return {'error': 'Item not found.'}, 404
        return item
