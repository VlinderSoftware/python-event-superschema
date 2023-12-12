from events import get_send_event_function
import json
from kafka import KafkaProducer
from purchase_order import PurchaseOrder
from uuid import uuid4 as uuid

def get_send_to_kafka_function(producer, topic):
    def send_to_kafka(event):
        producer.send(topic, json.dumps(event).encode())
    return send_to_kafka

producer = KafkaProducer()

send_event = get_send_event_function(get_send_to_kafka_function(producer, 'purchase-orders'), data_preprocessors={
    'PurchaseRequested': lambda a : a.serialize()
})

po = PurchaseOrder()
po.add_item('MAGNOLIA', 2)
po.add_item('RED_ROSE', 5)

send_event('PurchaseRequested', po, uid=str(uuid()))

producer.flush()
