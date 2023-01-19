from pulsar import Client, ConsumerType

client = Client('pulsar://localhost:6650')
consumer = client.subscribe(
    'persistent://public/default/tick',
    'i-am-shared',
    consumer_type=ConsumerType.Failover
)

while True:
    msg = consumer.receive()
    try:
        data = msg.data().decode('utf-8')
        print(f"Received message {data} id={msg.message_id()}")
        consumer.acknowledge(msg)
    except:
        consumer.negative_acknowledge(msg)

client.close()
