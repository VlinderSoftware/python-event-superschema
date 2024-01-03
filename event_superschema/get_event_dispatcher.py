from typing import Callable, Dict

from ._super_schema import _super_schema_validator

def get_event_dispatcher(
        err: Callable[[Dict[str, str]], None],
        handlers: Dict[str, Callable[[dict], None]]
        ) -> Callable[[dict], None]:
    '''Get an event dispatcher

    :param err: error handler. Receives an error message that, if it comes from this module, will contain at least an 'error' and a 'message' field
    :param handlers: Handlers for the event. For each event type to handle, it should have a function that takes the event as an argument. Only one handler per event is permitted. Exceptions are not caught. If no specific handler is available and a '__default__' handler is included in the handlers, that handler will be called by the dispatcher.
    :returns: a dispatcher that will validate incoming events against the super-schema and call the appropriate event handler if one is available.
    '''
    def _dispatch(event: dict) -> None:
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
    return _dispatch
