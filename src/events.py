from jsonschema import validators
from uuid import uuid4 as uuid

Validator = validators.Draft202012Validator

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
                "user": { "type": "string", "format": "uuid" },
                "token": { "type": "string" }
            },
            "required": [ "cid" ]
        },
        "data": { "type": "object" }
    },
    "required": [ "id", "type", "metadata" ]
}
_super_schema_validator = Validator(_super_schema)

def get_event_dispatcher(err: Callable[[Dict[str, str]], None], handlers: Dict[str, Callable[[dict], None]]) -> Callable[[dict], None]:
    def dispatch(event: dict) -> None:
        is_valid = _super_schema_validator.is_valid(event)
        if not is_valid:
            err({ 'error': 'SchemaMismatchError', 'message': 'Event does not match event schema' })
            return
        base_event_name = event['type'].rsplit(':', 1)[0]
        if event['type'] in handlers:
            handlers[event['type']](err, event)
        elif base_event_name in handlers:
            handlers[base_event_name](err, event)
        elif '__default__' in handlers and handlers['__default__']:
            handlers['__default__'](err, event)
    return dispatch

def _get_format_event_function(data_preprocessors=None):
    if not data_preprocessors:
        data_preprocessors = { '__default__': lambda a : a }
    def format_event(type, cid=None, id=None, pid=None, tid=None, uid=None, token=None, data=None):
        if data:
            if (not type in data_preprocessors or not data_preprocessors[type]) and (not '__default__' in data_preprocessors or not data_preprocessors['__default__']):
                raise Exception(f'No data formatter for type {type}, and data was provided')
            elif not type in data_preprocessors or not data_preprocessors[type]:
                formatted_data = data_preprocessors['__default__'](data)
            else:
                formatted_data = data_preprocessors[type](data)
        else:
            formatted_data = None
        event_id = id if id else str(uuid())
        metadata = {}
        metadata['cid'] = cid if cid else event_id
        metadata['tid'] = tid if tid else event_id
        if uid:
            metadata['uid'] = uid
        if token:
            metadata['token'] = token
        if pid:
            metadata['pid'] = pid
        
        formatted_event = {
            'id': event_id,
            'type': type,
            'metadata': metadata
        }
        if formatted_data:
            formatted_event['data'] = formatted_data
        
        return formatted_event
    return format_event

def get_send_event_function(send, data_preprocessors=None, pid=None):
    if not data_preprocessors:
        data_preprocessors = { '__default__': lambda a : a }
    format_event = _get_format_event_function(data_preprocessors)
    def send_event(event_type, event_data=None, cid=None, uid=None, token=None):
        formatted_event = format_event(type=event_type, cid=cid, pid=pid, uid=uid, token=token, data=event_data)
        send(formatted_event)
    return send_event