'''Validator for the super-schema'''
from jsonschema import validators

_Validator = validators.Draft202012Validator

_super_schema = {
    "type": "object",
    "properties": {
        "id": { "type": "string", "format": "uuid" },
        "type": { "type": "string" },
        "metadata": {
            "type": "object",
            "properties": {
                "cid": { "type": "string", "format": "uuid" },
                "tid": { "type": "string", "format": "uuid" },
                "pid": { "type": "string", "format": "uuid" },
                "uid": { "type": "string", "format": "uuid" },
                "token": { "type": "string" }
            },
            "required": [ "cid", "pid" ]
        },
        "data": { "type": "object" }
    },
    "required": [ "id", "type", "metadata" ]
}
_super_schema_validator = _Validator(_super_schema)
