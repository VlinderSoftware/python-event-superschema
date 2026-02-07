"""Step definitions for event formatting feature"""
from behave import given, when, then
from event_superschema import get_send_event_function
from event_superschema._super_schema import _super_schema_validator


@given('I have an event formatter')
def step_have_event_formatter(context):
    """Create an event formatter"""
    from uuid import uuid4 as uuid
    # Capture the formatted event
    def capture_send(event):
        context.formatted_event = event
    context.send_event = get_send_event_function(send=capture_send, pid=str(uuid()))


@when('I send a basic "{event_type}" event')
def step_send_basic_event(context, event_type):
    """Send a basic event with the given type"""
    context.send_event(event_type)


@when('I send an "{event_type}" event with data:')
def step_send_event_with_data(context, event_type):
    """Send an event with custom data"""
    data = {}
    for row in context.table:
        key = row['key']
        value = row['value']
        # Try to convert to number if possible
        try:
            value = float(value)
        except ValueError:
            pass
        data[key] = value
    
    context.send_event(event_type, event_data=data)


@when('I send an "{event_type}" event with correlation id "{cid}"')
def step_send_event_with_cid(context, event_type, cid):
    """Send an event with a custom correlation ID"""
    context.send_event(event_type, cid=cid)


@when('I send an "{event_type}" event with transaction id "{tid}"')
def step_send_event_with_tid(context, event_type, tid):
    """Send an event with a custom transaction ID"""
    # Note: The library auto-generates tid from the event id, so we need to use the internal formatter
    from event_superschema.get_send_event_function import _get_format_event_function
    from uuid import uuid4 as uuid
    formatter = _get_format_event_function(pid=str(uuid()))
    context.formatted_event = formatter(event_type=event_type, tid=tid)


@then('the formatted event should have a type "{event_type}"')
def step_check_event_type(context, event_type):
    """Verify the event has the correct type"""
    assert context.formatted_event['type'] == event_type, \
        f"Expected event type '{event_type}', got '{context.formatted_event['type']}'"


@then('the formatted event should have an id')
def step_check_event_has_id(context):
    """Verify the event has an ID"""
    assert 'id' in context.formatted_event, "Event should have an 'id' field"
    assert context.formatted_event['id'], "Event ID should not be empty"


@then('the formatted event should have metadata with correlation id')
def step_check_event_has_cid(context):
    """Verify the event has metadata with correlation ID"""
    assert 'metadata' in context.formatted_event, "Event should have 'metadata'"
    assert 'cid' in context.formatted_event['metadata'], "Metadata should have 'cid'"
    assert context.formatted_event['metadata']['cid'], "Correlation ID should not be empty"


@then('the formatted event should have metadata with transaction id')
def step_check_event_has_tid(context):
    """Verify the event has metadata with transaction ID"""
    assert 'metadata' in context.formatted_event, "Event should have 'metadata'"
    assert 'tid' in context.formatted_event['metadata'], "Metadata should have 'tid'"
    assert context.formatted_event['metadata']['tid'], "Transaction ID should not be empty"


@then('the formatted event should have metadata with correlation id "{cid}"')
def step_check_event_cid_value(context, cid):
    """Verify the event has the specified correlation ID"""
    assert context.formatted_event['metadata']['cid'] == cid, \
        f"Expected correlation ID '{cid}', got '{context.formatted_event['metadata']['cid']}'"


@then('the formatted event should have metadata with transaction id "{tid}"')
def step_check_event_tid_value(context, tid):
    """Verify the event has the specified transaction ID"""
    assert context.formatted_event['metadata']['tid'] == tid, \
        f"Expected transaction ID '{tid}', got '{context.formatted_event['metadata']['tid']}'"


@then('the formatted event should be valid according to the superschema')
def step_check_event_valid(context):
    """Verify the event is valid according to the superschema"""
    is_valid = _super_schema_validator.is_valid(context.formatted_event)
    assert is_valid, f"Event should be valid according to superschema. Event: {context.formatted_event}"


@then('the formatted event should contain data field "{field}" with value "{value}"')
def step_check_event_data_field(context, field, value):
    """Verify the event contains a specific data field with a value"""
    assert 'data' in context.formatted_event, "Event should have 'data' field"
    assert field in context.formatted_event['data'], f"Event data should have field '{field}'"
    
    actual_value = context.formatted_event['data'][field]
    # Try to convert expected value to match actual type
    try:
        value = float(value)
    except ValueError:
        pass
    
    assert actual_value == value, \
        f"Expected data field '{field}' to be '{value}', got '{actual_value}'"
