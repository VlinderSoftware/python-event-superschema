from events import get_event_dispatcher
import json
from kafka import KafkaConsumer
import logging
import purchase_order as po

def on_purchase_order_event(err, event):
    if (not 'uid' in event['metadata'] or not event['metadata']['uid']) and (not 'token' in event['metadata'] or not event['metadata']['token']) :
        err({ 'error': 'MissingUserError', 'message': 'Event does have uid (required for this event)' })
        return
    if not 'data' in event or not event['data']:
        err({ 'error': 'MissingDataError', 'message': 'Event does have data' })
        return
    is_valid = po.validator.is_valid(event['data'])
    if not is_valid:
        err({ 'error': 'SchemaMismatchError', 'message': 'Event data does not match event schema' })
        return
    # do something useful with the event 
    logging.warning(f'Received a purchase order event {event["id"]}')

consumer = KafkaConsumer('purchase-orders', group_id='services-order')
_handlers = {'PurchaseRequested': on_purchase_order_event}
dispatch = get_event_dispatcher(lambda err : logging.error(f'Error {err["error"]}: {err["message"]}', exc_info=err), _handlers)
for event in consumer:
    try:
        event_dict = json.loads(str(event.value, encoding='utf-8'))
        dispatch(event_dict)
    except:
        pass
