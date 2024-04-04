'''Test signing operations'''
import json
import jose
import os
from uuid import uuid4 as uuid
from event_superschema import get_jwe_event_dispatcher, get_jwe_send_event_function

from tests._error_schema_validator import _error_schema_validator

def generate_symmetric_secret(bits=256):
    '''Generate a random symmetric secret'''
    return os.urandom(bits // 8)

def test_get_signing_event_dispatcher():
    dispatcher = get_jwe_event_dispatcher(err=lambda a:a, handlers={}, key=generate_symmetric_secret())
    assert callable(dispatcher)

def test_get_signing_event_sender_A256GCM():
    send_called = False
    def send_mock(data):
        nonlocal send_called
        send_called = True
    sender = get_jwe_send_event_function(send=send_mock, pid=str(uuid()), key=generate_symmetric_secret(), algorithm='A256GCM')
    assert callable(sender)

def test_try_dispatch_unsigned_event_fails():
    err_called = False
    def err(error):
        nonlocal err_called
        assert _error_schema_validator.is_valid(error)
        assert error['error'] == 'InternalError'
        err_called = True
    dispatcher = get_jwe_event_dispatcher(err=err, handlers={}, key=generate_symmetric_secret())
    dispatcher({})
    assert err_called

def test_try_dispatch_badly_signed_event_fails_A256GCM():
    sender_secret = generate_symmetric_secret()
    deliberately_different_receiver_secret = generate_symmetric_secret()

    send_called = False
    received_data = None
    def send_mock(data):
        nonlocal send_called
        nonlocal received_data
        send_called = True
        received_data = data
    sender = get_jwe_send_event_function(send=send_mock, pid=str(uuid()), key=sender_secret, algorithm='A256GCM')
    sender(event_type="Test")
    assert send_called
    exception_caught = False
    # make sure this isn't still JSON
    try:
        _ = json.loads(received_data)
    except json.JSONDecodeError:
        exception_caught = True
    assert exception_caught
    dispatcher = get_jwe_event_dispatcher(err=lambda a:a, handlers={}, key=deliberately_different_receiver_secret)
    exception_caught = False
    try:
        dispatcher(received_data)
    except jose.exceptions.JWEError:
        exception_caught = True
    assert exception_caught

def test_try_dispatch_correctly_signed_event_A256GCM():
    shared_secret = generate_symmetric_secret()

    send_called = False
    received_data = None
    def send_mock(data):
        nonlocal send_called
        nonlocal received_data
        send_called = True
        received_data = data
    sender = get_jwe_send_event_function(send=send_mock, pid=str(uuid()), key=shared_secret, algorithm='A256GCM')
    sender(event_type="Test")
    assert send_called
    exception_caught = False
    # make sure this isn't still JSON
    try:
        _ = json.loads(received_data)
    except json.JSONDecodeError:
        exception_caught = True
    assert exception_caught
    handler_called = False
    def event_handler(err, event):
        nonlocal handler_called
        handler_called = True
    dispatcher = get_jwe_event_dispatcher(err=lambda a:a, handlers={"Test": event_handler}, key=shared_secret)
    exception_caught = False
    try:
        dispatcher(received_data)
    except jose.exceptions.JWEError:
        exception_caught = True
    assert not exception_caught
    assert handler_called
