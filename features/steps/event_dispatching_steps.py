"""Step definitions for event dispatching feature"""
from behave import given, when, then
from event_superschema import get_event_dispatcher
from uuid import uuid4 as uuid


@given('I have an event dispatcher with a handler for "{event_type}"')
def step_have_dispatcher_with_handler(context, event_type):
    """Create an event dispatcher with a handler for a specific event type"""
    context.handler_called = {}
    context.error_called = False
    context.error_message = None
    
    def handler(err, event):
        context.handler_called[event_type] = True
    
    def error_handler(error):
        context.error_called = True
        context.error_message = error
    
    context.dispatcher = get_event_dispatcher(
        err=error_handler,
        handlers={event_type: handler}
    )


@given('I have an event dispatcher with an error handler')
def step_have_dispatcher_with_error_handler(context):
    """Create an event dispatcher with an error handler"""
    context.error_called = False
    context.error_message = None
    
    def error_handler(error):
        context.error_called = True
        context.error_message = error
    
    context.dispatcher = get_event_dispatcher(
        err=error_handler,
        handlers={}
    )


@given('I have an event dispatcher with a default handler')
def step_have_dispatcher_with_default_handler(context):
    """Create an event dispatcher with a default handler"""
    context.default_handler_called = False
    context.handler_called = {}
    context.error_called = False
    
    def default_handler(err, event):
        context.default_handler_called = True
    
    def error_handler(error):
        context.error_called = True
        context.error_message = error
    
    context.dispatcher = get_event_dispatcher(
        err=error_handler,
        handlers={'__default__': default_handler}
    )


@given('I have no specific handler for "{event_type}"')
def step_have_no_handler_for_event(context, event_type):
    """Verify there's no specific handler for the event type"""
    # This is just a documentation step, no action needed
    pass


@given('I have an event dispatcher with handlers for "{event_type1}" and "{event_type2}"')
def step_have_dispatcher_with_multiple_handlers(context, event_type1, event_type2):
    """Create an event dispatcher with handlers for multiple event types"""
    context.handler_called = {}
    context.error_called = False
    
    def handler1(err, event):
        context.handler_called[event_type1] = True
    
    def handler2(err, event):
        context.handler_called[event_type2] = True
    
    def error_handler(error):
        context.error_called = True
        context.error_message = error
    
    context.dispatcher = get_event_dispatcher(
        err=error_handler,
        handlers={
            event_type1: handler1,
            event_type2: handler2
        }
    )


@when('I dispatch a valid "{event_type}" event')
def step_dispatch_valid_event(context, event_type):
    """Dispatch a valid event"""
    event = {
        'type': event_type,
        'id': str(uuid()),
        'metadata': {
            'cid': str(uuid()),
            'pid': str(uuid()),
        }
    }
    context.dispatcher(event)


@when('I dispatch an invalid event missing required fields')
def step_dispatch_invalid_event(context):
    """Dispatch an invalid event"""
    invalid_event = {}
    context.dispatcher(invalid_event)


@then('the "{event_type}" handler should be called')
def step_check_handler_called(context, event_type):
    """Verify a specific handler was called"""
    assert context.handler_called.get(event_type, False), \
        f"Handler for '{event_type}' should have been called"


@then('the error handler should be called with a schema mismatch error')
def step_check_error_handler_called_schema_mismatch(context):
    """Verify the error handler was called with a schema mismatch error"""
    assert context.error_called, "Error handler should have been called"
    assert context.error_message is not None, "Error message should not be None"
    assert 'error' in context.error_message, "Error message should have 'error' field"
    assert context.error_message['error'] == 'SchemaMismatchError', \
        f"Expected SchemaMismatchError, got {context.error_message['error']}"


@then('the default handler should be called')
def step_check_default_handler_called(context):
    """Verify the default handler was called"""
    assert context.default_handler_called, "Default handler should have been called"
