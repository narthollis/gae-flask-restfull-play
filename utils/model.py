from __future__ import absolute_import, division, print_function

from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb

from utils import fields as fields

FIELD_MAP = {
    ndb.StringProperty: fields.String,
    ndb.DateTimeProperty: fields.DateTime,
    ndb.IntegerProperty: fields.Integer,
    ndb.IndexProperty: fields.String
}


class Model(ndb.Model):
    _fields = None

    def __marshallable__(self):
        val = dict(self.__dict__)

        val['id'] = self.key.id()
        return val

    @property
    def id(self):
        return self.key.id()

    @classmethod
    def fields(cls, endpoint=None):
        if cls._fields is not None:
            return cls._fields

        cls._fields = dict()

        if endpoint is not None:
            cls._fields['href'] = fields.Url(endpoint)

        cls._fields['id'] = fields.String

        for key, value in cls._properties.items():
            t = type(value)
            if t in FIELD_MAP.keys():
                cls._fields[key] = FIELD_MAP[t]

        return cls._fields

    @classmethod
    def get_by_key(cls, key):
        key = ndb.Key(urlsafe=key)
        return super(Model, cls).get_by_id(key.id())

    @classmethod
    def fetch_page(cls, page_size, cursor=None):
        """
        :param page_size: At most this many results will be returned.
        :param cursor: urlsafe cursor string
        :return: Tuple (results, cursor, more, total)
        """
        q = super(Model, cls).query()

        cur = Cursor(urlsafe=cursor)

        totals_future = q.count_async()
        fetch_future = q.fetch_page_async(page_size, start_cursor=cur)

        ndb.Future.wait_all([totals_future, fetch_future])

        total = totals_future.get_result()
        fetch = fetch_future.get_result()

        return fetch[0], fetch[1], fetch[2], total
