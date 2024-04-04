from jsonschema import validators

Validator = validators.Draft202012Validator

_error_schema = {
    'type': 'object',
    'properties': {
        'error': { 'type': 'string', 'pattern': '^[A-Z][A-Za-z]*$' },
        'message': { 'type': 'string' },
    },
    'required': ['error', 'message']
}
_error_schema_validator = Validator(_error_schema)
