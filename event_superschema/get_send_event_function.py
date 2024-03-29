'''
Get the send_event function, which formats the event and sends it to the bus, taking care of
most of the boilerplate
'''
from uuid import uuid4 as uuid
from typing import Callable, Dict, Optional

def _get_format_event_function(
    data_preprocessors:Dict[str, Callable[[any],dict]]=None,
    pid:Optional[str]=None
    ) -> Callable[
        [str,
         Optional[str],
         Optional[str],
         Optional[str],
         Optional[str],
         Optional[str],
         Optional[str]
        ],
        dict
    ]:
    if pid is None:
        pid = str(uuid())
    if data_preprocessors is None:
        data_preprocessors = { '__default__': lambda a : a }
    elif '__default__' not in data_preprocessors or data_preprocessors['__default__'] is None:
        data_preprocessors['__default__'] = lambda a : a
    else:
        pass
    # pylint: disable=locally-disabled, too-many-arguments
    def format_event(
            event_type:str,
            cid:Optional[str]=None,
            event_id:Optional[str]=None,
            tid:Optional[str]=None,
            uid:Optional[str]=None,
            token:Optional[str]=None,
            data:Optional[str]=None
            ) -> dict:
        if data is not None:
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
        if formatted_data is not None:
            formatted_event['data'] = formatted_data

        return formatted_event
    return format_event

def get_send_event_function(
    send:Callable[[dict], None],
    pid:str,
    data_preprocessors:Optional[Dict[str, Callable[[dict], None]]]=None) -> Callable[[
    str,Optional[any],Optional[str],Optional[str],Optional[str]],None]:
    '''Get a function to send properly formatted events

    :param send: a generic function to send events on the event bus, once they're properly
                 formatted. Should expect a dict and not return anything.
    :param pid: producer ID
    :param data_preprocessors: optional dict mapping event types to their data preprocessors.
        The data preprocessor should convert the event data to a serializable dict conforming
        to the appropriate schema
    '''
    if not data_preprocessors:
        data_preprocessors = { '__default__': lambda a : a }
    format_event = _get_format_event_function(data_preprocessors=data_preprocessors, pid=pid)
    def send_event(
            event_type:str,
            event_data:Optional[any]=None,
            cid:Optional[str]=None,
            uid:Optional[str]=None,
            token:Optional[str]=None,
        ) -> None:
        formatted_event = format_event(
            event_type=event_type,
            cid=cid,
            uid=uid,
            token=token,
            data=event_data
            )
        send(formatted_event)
    return send_event
