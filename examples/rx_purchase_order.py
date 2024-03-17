'''Example for receiving purchase orders from a bus'''
from event_superschema import get_event_dispatcher
import json
from kafka import KafkaConsumer
import logging
import purchase_order as po

def on_purchase_order_event(err, the_event):
    if ((not 'uid' in the_event['metadata'] or not the_event['metadata']['uid'])
        and (not 'token' in the_event['metadata'] or not the_event['metadata']['token'])):
        err({ 'error': 'MissingUserError', 'message': 'Event does have uid (required for this event)' })
        return
    if not 'data' in the_event or not the_event['data']:
        err({ 'error': 'MissingDataError', 'message': 'Event does have data' })
        return
    is_valid = po.validator.is_valid(the_event['data'])
    if not is_valid:
        err({ 'error': 'SchemaMismatchError', 'message': 'Event data does not match event schema' })
        return
    # do something useful with the event
    logging.warning('Received a purchase order event %s', the_event['id'])

consumer = KafkaConsumer('purchase-orders', group_id='services-order')
_handlers = {'PurchaseRequested': on_purchase_order_event}
dispatch = get_event_dispatcher(
    lambda err : logging.error('Error %s: %s', err['error'], err['message'], exc_info=err),
    _handlers
    )
for event in consumer:
    try:
        event_dict = json.loads(str(event.value, encoding='utf-8'))
        dispatch(event_dict)
    # pylint: disable=bare-except
    except:
        pass
