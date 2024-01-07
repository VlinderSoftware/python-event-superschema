'''
Support for a generic super-schema for event handling.
'''
from uuid import uuid4 as uuid
from typing import Callable, Dict, Optional

from .super_schema import _super_schema_validator

def get_event_dispatcher(
        err: Callable[[Dict[str, str]], None],
        handlers: Dict[str, Callable[[dict], None]]
        ) -> Callable[[dict], None]:
    '''Get an event dispatcher

    :param err: error handler. Receives an error message that, if it comes from this module, will
                contain at least an 'error' and a 'message' field
    :param handlers: Handlers for the event. For each event type to handle, it should have a
                     function that takes the event as an argument. Only one handler per event
                     is permitted. Exceptions are not caught. If no specific handler is
                     available and a '__default__' handler is included in the handlers, that
                     handler will be called by the dispatcher.
    :returns: a dispatcher that will validate incoming events against the super-schema and call the
              appropriate event handler if one is available.
    '''
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

def _get_format_event_function(
    data_preprocessors:Dict[str, Callable[[any],dict]]=None) -> Callable[
    [str, Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]],dict]:
    if data_preprocessors is None:
        data_preprocessors = { '__default__': lambda a : a }
    elif data_preprocessors['__default__'] is None:
        data_preprocessors['__default__'] = lambda a : a
    else:
        pass
    def format_event(
            event_type:str,
            cid:Optional[str]=None,
            event_id:Optional[str]=None,
            pid:Optional[str]=None,
            tid:Optional[str]=None,
            uid:Optional[str]=None,
            token:Optional[str]=None,
            data:Optional[str]=None
            ):dict:
        if data:
            if not event_type in data_preprocessors or not data_preprocessors[event_type]:
                formatted_data = data_preprocessors['__default__'](data)
            else:
                formatted_data = data_preprocessors[event_type](data)
        else:
            formatted_data = None
        event_id = event_id if event_id else str(uuid())
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
            'type': event_type,
            'metadata': metadata
        }
        if formatted_data:
            formatted_event['data'] = formatted_data

        return formatted_event
    return format_event

def get_send_event_function(
    send:Callable[[dict], None],
    data_preprocessors:Optional[Dict[str, Callable[[dict], None]]]=None,
    pid:Optional[str]=None) -> Callable[[
    str,Optional[any],Optional[str],Optional[str],Optional[str]],None]:
    '''Get a function to send properly formatted events
    
    :param send: a generic function to send events on the event bus, once they're properly
                 formatted. Should expect a dict and not return anything.
    :param data_preprocessors: optional dict mapping event types to their data preprocessors. The data preprocessor should convert the event data to a serializable dict conforming to the appropriate schema
    :param pid: optional producer ID
    '''
    if not data_preprocessors:
        data_preprocessors = { '__default__': lambda a : a }
    format_event = _get_format_event_function(data_preprocessors)
    def send_event(event_type:str, event_data:Optional[any]=None, cid:Optional[str]=None, uid:Optional[str]=None, token:Optional[str]=None) -> None:
        formatted_event = format_event(
            event_type=event_type,
            cid=cid,
            pid=pid,
            uid=uid,
            token=token,
            data=event_data
            )
        send(formatted_event)
    return send_event
