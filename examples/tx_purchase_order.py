'''Example code for transmitting events'''
from event_superschema import get_send_event_function
import json
from kafka import KafkaProducer
from purchase_order import PurchaseOrder
from uuid import uuid4 as uuid

def get_send_to_kafka_function(producer, topic):
    def send_to_kafka(event):
        producer.send(topic, json.dumps(event).encode())
    return send_to_kafka

if __name__ == '__main__':
    kafka_producer = KafkaProducer()
    pid = str(uuid())

    send_event = get_send_event_function(
        get_send_to_kafka_function(kafka_producer, 'purchase-orders'),
        pid=pid,
        data_preprocessors={
            'PurchaseRequested': lambda a : a.serialize()
        }
    )

    po = PurchaseOrder()
    po.add_item('MAGNOLIA', 2)
    po.add_item('RED_ROSE', 5)

    send_event('PurchaseRequested', po, uid=str(uuid()))

    kafka_producer.flush()
