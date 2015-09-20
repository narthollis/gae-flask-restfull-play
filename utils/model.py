from __future__ import absolute_import, division, print_function

from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb

from utils import fields as fields


FIELD_MAP = {
    ndb.StringProperty: fields.String,
    ndb.DateTimeProperty: fields.DateTime
}


class Model(ndb.Model):
    _fields = None

    def __marshallable__(self):
        s = super(Model, self)

        if hasattr(s, '__marshallable__'):
            val = s.__marshallable__()
        else:
            val = dict(self.__dict__)

        val['key'] = self.key.urlsafe()
        return val

    @classmethod
    def fields(cls, endpoint=None):
        if cls._fields is not None:
            return cls._fields

        cls._fields = dict(key=fields.Key)

        if endpoint is not None:
            cls._fields['href'] = fields.Url(endpoint)

        for key, value in cls.__dict__.items():
            t = type(value)
            if t in FIELD_MAP.keys():
                cls._fields[key] = FIELD_MAP[t]

        return cls._fields

    @classmethod
    def get_by_key(cls, key):
        key = ndb.Key(urlsafe=key)
        return super(Model, cls).get_by_id(key.id())

    @classmethod
    def fetch_page(cls, count, cursor=None):
        cur = Cursor(urlsafe=cursor)

        return super(Model, cls).query().fetch_page(count, start_cursor=cur)
