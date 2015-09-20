from __future__ import absolute_import, division, print_function
from flask_restful.fields import MarshallingException #, to_marshallable_type
from flask_restful.fields import *


class Key(Raw):
    def format(self, value):
        try:
            return value.urlsafe()
        except ValueError as ve:
            raise MarshallingException(ve)


# class UrlForNDBModal(Url):
#     def output(self, key, obj):
#         data = to_marshallable_type(obj)
#         data.key = obj.key.urlsafe()
#
#         return super(UrlForNDBModal, self).output(key, obj)
