from datetime import datetime
from jsonschema import validators
from uuid import uuid4 as uuid

Validator = validators.Draft202012Validator

_purchase_order_schema = {
    "type": "object",
    "properties": {
        "id": { "type": "string", "format": "uuid" },
        "requestDate": { "type": "string", "format": "date" },
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": { "type": "string" },
                    "code": { "type": "string" },
                    "qty": { "type": "integer", "minimum": 0 },
                    "price": { "type": "number", "minimum": 0 },
                    "discount": { "type": "number", "minimum": 0, "maximum": 100 }
                }
            },
            "required": ["code", "qty"],
            "minItems": 1,
            "uniqueItems": True
        }
    },
    "required": [ "requestDate", "items" ]
}
validator = Validator(_purchase_order_schema)

class PurchaseOrder:
    def __init__(self, id=None, request_date=None, items=None):
        self._id = str(uuid()) if not id else id
        self._request_date = datetime.today().strftime('%Y-%m-%d') if not request_date else request_date
        self._items = [] if not items else items

    def add_item(self, code, qty, name=None, price=None, discount=None):
        item = { 'code': code, 'qty': qty }
        if name:
            item['name'] = name
        if price:
            item['price'] = price
        if discount:
            item['discount'] = discount
        self._items.append(item)

    def serialize(self):
        serialized = {
            'id': self._id,
            'requestDate': self._request_date,
            'items': self._items
        }
        return serialized
    
    @classmethod
    def deserialize(dict):
        assert(validator.is_valid(dict))
        return PurchaseOrder(id=dict['id'], request_date=dict['requestDate'], items=dict['items'])
