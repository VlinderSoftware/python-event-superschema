'''Test event formatting'''
from event_superschema.get_send_event_function import _get_format_event_function
from event_superschema._super_schema import _super_schema_validator
from uuid import uuid4 as uuid

def test_get_format_event_function_no_params():
    '''Get the format event function'''
    format_event = _get_format_event_function()
    assert callable(format_event)
    formatted_event = format_event('TheEventType')
    assert _super_schema_validator.is_valid(formatted_event)
    assert formatted_event['type'] == 'TheEventType'
    assert formatted_event['id'] == formatted_event['metadata']['cid']
    assert formatted_event['id'] == formatted_event['metadata']['tid']

def test_get_format_event_function_no_formatters():
    '''Get the format event function'''
    format_event = _get_format_event_function(data_preprocessors={})
    assert callable(format_event)
    formatted_event = format_event('TheEventType')
    assert _super_schema_validator.is_valid(formatted_event)
    assert formatted_event['type'] == 'TheEventType'
    assert formatted_event['id'] == formatted_event['metadata']['cid']
    assert formatted_event['id'] == formatted_event['metadata']['tid']

def test_get_format_event_function_default_is_none():
    '''Get the format event function'''
    format_event = _get_format_event_function(data_preprocessors={'__default__': None})
    assert callable(format_event)
    formatted_event = format_event('TheEventType')
    assert _super_schema_validator.is_valid(formatted_event)
    assert formatted_event['type'] == 'TheEventType'
    assert formatted_event['id'] == formatted_event['metadata']['cid']
    assert formatted_event['id'] == formatted_event['metadata']['tid']

def test_get_format_event_function_just_default_formatter():
    '''Get the format event function'''
    default_formatter_called = False
    def default_formatter(a):
        nonlocal default_formatter_called
        default_formatter_called = True
        return a
    format_event = _get_format_event_function(data_preprocessors={ '__default__': default_formatter })
    assert callable(format_event)
    formatted_event = format_event('TheEventType')
    assert not default_formatter_called # no data provided
    assert _super_schema_validator.is_valid(formatted_event)
    assert formatted_event['type'] == 'TheEventType'
    assert formatted_event['id'] == formatted_event['metadata']['cid']
    assert formatted_event['id'] == formatted_event['metadata']['tid']

def test_get_format_event_function_just_default_formatter():
    '''Get the format event function'''
    default_formatter_called = False
    def default_formatter(a):
        nonlocal default_formatter_called
        default_formatter_called = True
        return a
    format_event = _get_format_event_function(data_preprocessors={ '__default__': default_formatter })
    assert callable(format_event)
    formatted_event = format_event('TheEventType', data={})
    assert default_formatter_called
    assert _super_schema_validator.is_valid(formatted_event)
    assert formatted_event['type'] == 'TheEventType'
    assert formatted_event['id'] == formatted_event['metadata']['cid']
    assert formatted_event['id'] == formatted_event['metadata']['tid']
    assert 'data' in formatted_event

def test_get_format_event_function_default_and_named_formatter():
    '''Get the format event function'''
    default_formatter_called = False
    named_formatter_called = False
    def default_formatter(a):
        nonlocal default_formatter_called
        default_formatter_called = True
        return a
    def named_formatter(a):
        nonlocal named_formatter_called
        named_formatter_called = True
        return a
    format_event = _get_format_event_function(
        data_preprocessors={
            '__default__': default_formatter,
            'TheEventType': named_formatter,
            }
        )
    assert callable(format_event)
    formatted_event = format_event('TheEventType', data={})
    assert not default_formatter_called
    assert named_formatter_called
    assert _super_schema_validator.is_valid(formatted_event)
    assert formatted_event['type'] == 'TheEventType'
    assert formatted_event['id'] == formatted_event['metadata']['cid']
    assert formatted_event['id'] == formatted_event['metadata']['tid']
    assert 'data' in formatted_event

def test_get_format_event_function_with_pid():
    '''Get the format event function'''
    pid = str(uuid())
    format_event = _get_format_event_function(pid=pid)
    assert callable(format_event)
    formatted_event = format_event('TheEventType')
    assert _super_schema_validator.is_valid(formatted_event)
    assert formatted_event['type'] == 'TheEventType'
    assert formatted_event['id'] == formatted_event['metadata']['cid']
    assert formatted_event['id'] == formatted_event['metadata']['tid']
    assert formatted_event['metadata']['pid'] == pid

def test_get_format_event_function_no_formatters_with_pid():
    '''Get the format event function'''
    pid = str(uuid())
    format_event = _get_format_event_function(data_preprocessors={}, pid=pid)
    assert callable(format_event)
    formatted_event = format_event('TheEventType')
    assert _super_schema_validator.is_valid(formatted_event)
    assert formatted_event['type'] == 'TheEventType'
    assert formatted_event['id'] == formatted_event['metadata']['cid']
    assert formatted_event['id'] == formatted_event['metadata']['tid']
    assert formatted_event['metadata']['pid'] == pid

def test_get_format_event_function_default_is_none_with_pid():
    '''Get the format event function'''
    pid = str(uuid())
    format_event = _get_format_event_function(data_preprocessors={'__default__': None}, pid=pid)
    assert callable(format_event)
    formatted_event = format_event('TheEventType')
    assert _super_schema_validator.is_valid(formatted_event)
    assert formatted_event['type'] == 'TheEventType'
    assert formatted_event['id'] == formatted_event['metadata']['cid']
    assert formatted_event['id'] == formatted_event['metadata']['tid']
    assert formatted_event['metadata']['pid'] == pid

def test_get_format_event_function_just_default_formatter_with_pid():
    '''Get the format event function'''
    default_formatter_called = False
    def default_formatter(a):
        nonlocal default_formatter_called
        default_formatter_called = True
        return a
    pid = str(uuid())
    format_event = _get_format_event_function(data_preprocessors={ '__default__': default_formatter }, pid=pid)
    assert callable(format_event)
    formatted_event = format_event('TheEventType')
    assert not default_formatter_called # no data provided
    assert _super_schema_validator.is_valid(formatted_event)
    assert formatted_event['type'] == 'TheEventType'
    assert formatted_event['id'] == formatted_event['metadata']['cid']
    assert formatted_event['id'] == formatted_event['metadata']['tid']
    assert formatted_event['metadata']['pid'] == pid

def test_get_format_event_function_just_default_formatter_with_pid():
    '''Get the format event function'''
    default_formatter_called = False
    def default_formatter(a):
        nonlocal default_formatter_called
        default_formatter_called = True
        return a
    pid = str(uuid())
    format_event = _get_format_event_function(data_preprocessors={ '__default__': default_formatter }, pid=pid)
    assert callable(format_event)
    formatted_event = format_event('TheEventType', data={})
    assert default_formatter_called
    assert _super_schema_validator.is_valid(formatted_event)
    assert formatted_event['type'] == 'TheEventType'
    assert formatted_event['id'] == formatted_event['metadata']['cid']
    assert formatted_event['id'] == formatted_event['metadata']['tid']
    assert formatted_event['metadata']['pid'] == pid
    assert 'data' in formatted_event

def test_get_format_event_function_default_and_named_formatter_with_pid():
    '''Get the format event function'''
    default_formatter_called = False
    named_formatter_called = False
    def default_formatter(a):
        nonlocal default_formatter_called
        default_formatter_called = True
        return a
    def named_formatter(a):
        nonlocal named_formatter_called
        named_formatter_called = True
        return a
    pid = str(uuid())
    format_event = _get_format_event_function(
        data_preprocessors={
            '__default__': default_formatter,
            'TheEventType': named_formatter,
            },
        pid=pid
        )
    assert callable(format_event)
    formatted_event = format_event('TheEventType', data={})
    assert not default_formatter_called
    assert named_formatter_called
    assert _super_schema_validator.is_valid(formatted_event)
    assert formatted_event['type'] == 'TheEventType'
    assert formatted_event['id'] == formatted_event['metadata']['cid']
    assert formatted_event['id'] == formatted_event['metadata']['tid']
    assert formatted_event['metadata']['pid'] == pid
    assert 'data' in formatted_event

def test_get_format_event_function_default_and_named_formatter_with_pid_and_uid():
    '''Get the format event function'''
    default_formatter_called = False
    named_formatter_called = False
    def default_formatter(a):
        nonlocal default_formatter_called
        default_formatter_called = True
        return a
    def named_formatter(a):
        nonlocal named_formatter_called
        named_formatter_called = True
        return a
    pid = str(uuid())
    uid = str(uuid())
    format_event = _get_format_event_function(
        data_preprocessors={
            '__default__': default_formatter,
            'TheEventType': named_formatter,
            },
        pid=pid
        )
    assert callable(format_event)
    formatted_event = format_event('TheEventType', data={}, uid=uid)
    assert not default_formatter_called
    assert named_formatter_called
    assert _super_schema_validator.is_valid(formatted_event)
    assert formatted_event['type'] == 'TheEventType'
    assert formatted_event['id'] == formatted_event['metadata']['cid']
    assert formatted_event['id'] == formatted_event['metadata']['tid']
    assert formatted_event['metadata']['pid'] == pid
    assert formatted_event['metadata']['uid'] == uid
    assert 'data' in formatted_event

def test_get_format_event_function_default_and_named_formatter_with_pid_and_uid_and_token():
    '''Get the format event function'''
    default_formatter_called = False
    named_formatter_called = False
    def default_formatter(a):
        nonlocal default_formatter_called
        default_formatter_called = True
        return a
    def named_formatter(a):
        nonlocal named_formatter_called
        named_formatter_called = True
        return a
    pid = str(uuid())
    uid = str(uuid())
    token = str(uuid())
    format_event = _get_format_event_function(
        data_preprocessors={
            '__default__': default_formatter,
            'TheEventType': named_formatter,
            },
        pid=pid
        )
    assert callable(format_event)
    formatted_event = format_event('TheEventType', data={}, uid=uid, token=token)
    assert not default_formatter_called
    assert named_formatter_called
    assert _super_schema_validator.is_valid(formatted_event)
    assert formatted_event['type'] == 'TheEventType'
    assert formatted_event['id'] == formatted_event['metadata']['cid']
    assert formatted_event['id'] == formatted_event['metadata']['tid']
    assert formatted_event['metadata']['pid'] == pid
    assert formatted_event['metadata']['uid'] == uid
    assert formatted_event['metadata']['token'] == token
    assert 'data' in formatted_event

