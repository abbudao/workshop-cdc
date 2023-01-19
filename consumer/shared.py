from pulsar import Client, ConsumerType
from pprint import pprint
import json
import re


debezium_prefix = "workshop"
client = Client('pulsar://localhost:6650')
consumer = client.subscribe(

    re.compile('persistent://public/default/outbox.event.user-created'),
    'i-am-shared',
    consumer_type=ConsumerType.Shared
)

while True:
    msg = consumer.receive()
    try:
        data = msg.data().decode('utf-8')
        print(f"Received message:")
        pprint(json.loads(data))
        consumer.acknowledge(msg)
    except:
        consumer.negative_acknowledge(msg)

client.close()
