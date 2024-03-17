'''Example purchase order class and suport code'''
from typing import Dict
from datetime import datetime
from uuid import uuid4 as uuid

from jsonschema import validators

Validator = validators.Draft202012Validator

_purchase_order_schema = {
    'type': 'object',
    'properties': {
        'id': { 'type': 'string', 'format': 'uuid' },
        'requestDate': { 'type': 'string', 'format': 'date' },
        'items': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'name': { 'type': 'string' },
                    'code': { 'type': 'string' },
                    'qty': { 'type': 'integer', 'minimum': 0 },
                    'price': { 'type': 'number', 'minimum': 0 },
                    'discount': { 'type': 'number', 'minimum': 0, 'maximum': 100 }
                }
            },
            'required': ['code', 'qty'],
            'minItems': 1,
            'uniqueItems': True
        }
    },
    'required': [ 'requestDate', 'items' ]
}
validator = Validator(_purchase_order_schema)

class PurchaseOrder:
    '''Example purchase order class'''
    def __init__(self, po_id=None, request_date=None, items=None):
        self._id = str(uuid()) if not po_id else po_id
        if not request_date:
            self._request_date = datetime.today().strftime('%Y-%m-%d')
        else:
            self._request_date = request_date
        self._items = [] if not items else items

    def add_item(self, code, qty, name=None, price=None, discount=None):
        '''Add an item to the purchase order'''
        item = { 'code': code, 'qty': qty }
        if name:
            item['name'] = name
        if price:
            item['price'] = price
        if discount:
            item['discount'] = discount
        self._items.append(item)

    def serialize(self):
        '''Serialize the purchase order to a dict'''
        serialized = {
            'id': self._id,
            'requestDate': self._request_date,
            'items': self._items
        }
        return serialized

    @classmethod
    def deserialize(cls, purchase_order:Dict[str,any]):
        '''Deserialize a dict to a purchase order'''
        assert validator.is_valid(purchase_order)
        return PurchaseOrder(
            po_id=purchase_order['id'],
            request_date=purchase_order['requestDate'],
            items=purchase_order['items'],
            )
