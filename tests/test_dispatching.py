'''Test event dispatching'''
from uuid import uuid4 as uuid
from jsonschema import validators
from event_superschema import get_event_dispatcher

Validator = validators.Draft202012Validator

_error_schema = {
    "type": "object",
    "properties": {
        "error": { "type": "string", "pattern": "^[A-Z][A-Za-z]*$" },
        "message": { "type": "string" },
    }
}
_error_schema_validator = Validator(_error_schema)

def test_get_event_dispatcher():
    '''Get a minimal event dispatcher'''
    dispatcher = get_event_dispatcher(err=lambda a: a, handlers={})
    assert callable(dispatcher)

def test_dispatcher_validates_against_schema_expect_fail_missing_everything():
    '''Validate that the dispatcher validates against the event schema'''
    err_called = False
    def err(error):
        nonlocal err_called
        assert _error_schema_validator.is_valid(error)
        assert error['error'] == 'SchemaMismatchError'
        err_called = True
    dispatcher = get_event_dispatcher(err=err, handlers={})
    dispatcher({})
    assert(err_called)

def test_dispatcher_validates_against_schema_expect_pass():
    '''
    Validate that a valid event passes inspection
    We don't check that the handler is called here
    '''
    err_called = False
    def err(_):
        nonlocal err_called
        err_called = True

    dispatcher = get_event_dispatcher(err=err, handlers={})
    minimal_event = {
        'type': 'EventType',
        'id': str(uuid()),
        'metadata': {
            'cid': str(uuid()),
        }
    }
    dispatcher(minimal_event)
    assert not err_called

def test_dispatcher_calls_default_handler():
    '''
    Validate that a valid event for which we do not have a specific
    handler is passed to the default handler, if one is set
    '''
    minimal_event = {
        'type': 'EventType',
        'id': str(uuid()),
        'metadata': {
            'cid': str(uuid()),
        }
    }

    err_called = False
    def err(_):
        nonlocal err_called
        err_called = True

    handler_called = False
    def default_handler(_, event):
        nonlocal handler_called
        assert event is minimal_event
        handler_called = True
    handlers = {
        '__default__': default_handler,
    }
    dispatcher = get_event_dispatcher(err=err, handlers=handlers)
    dispatcher(minimal_event)
    assert not err_called
    assert handler_called

def test_dispatcher_calls_named_handler():
    '''
    Validate that a valid event is passed to the named handler if one
    is available, and is not passed to the default handler in that 
    case
    '''
    minimal_event = {
        'type': 'EventType',
        'id': str(uuid()),
        'metadata': {
            'cid': str(uuid()),
        }
    }

    err_called = False
    def err(_):
        nonlocal err_called
        err_called = True

    default_handler_called = False
    def default_handler(_, __):
        nonlocal default_handler_called
        default_handler_called = True

    named_handler_called = False
    def named_handler(_, event):
        nonlocal named_handler_called
        assert event is minimal_event
        named_handler_called = True

    handlers = {
        '__default__': default_handler,
        'EventType': named_handler,
    }
    dispatcher = get_event_dispatcher(err=err, handlers=handlers)
    dispatcher(minimal_event)
    assert not err_called
    assert not default_handler_called
    assert named_handler_called

def test_dispatcher_calls_named_base_handler():
    '''
    Validate that a valid event is passed to the handler that has the
    basename of the event if an exact version is not available
    '''
    minimal_event = {
        'type': 'EventType:1',
        'id': str(uuid()),
        'metadata': {
            'cid': str(uuid()),
        }
    }

    err_called = False
    def err(_):
        nonlocal err_called
        err_called = True

    default_handler_called = False
    def default_handler(_, __):
        nonlocal default_handler_called
        default_handler_called = True

    named_handler_called = False
    def named_handler(_, event):
        nonlocal named_handler_called
        assert event is minimal_event
        named_handler_called = True

    handlers = {
        '__default__': default_handler,
        'EventType': named_handler,
    }
    dispatcher = get_event_dispatcher(err=err, handlers=handlers)
    dispatcher(minimal_event)
    assert not err_called
    assert not default_handler_called
    assert named_handler_called

def test_dispatcher_calls_exact_named_handler():
    '''
    Validate that a valid event is passed to the exact handler, and not
    to the base name handler, if one is available
    '''
    minimal_event = {
        'type': 'EventType:1',
        'id': str(uuid()),
        'metadata': {
            'cid': str(uuid()),
        }
    }

    err_called = False
    def err():
        nonlocal err_called
        err_called = True

    default_handler_called = False
    def default_handler(_, __):
        nonlocal default_handler_called
        default_handler_called = True

    named_handler_called = False
    def named_handler(_, __):
        nonlocal named_handler_called
        named_handler_called = True

    exact_named_handler_called = False
    def exact_named_handler(_, event):
        nonlocal exact_named_handler_called
        assert event is minimal_event
        exact_named_handler_called = True

    handlers = {
        '__default__': default_handler,
        'EventType': named_handler,
        'EventType:1': exact_named_handler,
    }
    dispatcher = get_event_dispatcher(err=err, handlers=handlers)
    dispatcher(minimal_event)
    assert not err_called
    assert not default_handler_called
    assert not named_handler_called
    assert exact_named_handler_called
