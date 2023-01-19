import pulsar
import json
import time
from random import choice, random

client = pulsar.Client("pulsar://localhost:6650")

producer = client.create_producer("persistent://public/default/tick")

symbols = [
    "PETR4",
    "VALE3",
    "CIEL3",
    "PETR5",
    "VALE5",
    "CIEL8",
    "AAPL",
    "MSFT",
]

while True:
    data = {
        "symbol": choice(symbols),
        "value": random() * 1000
    }

    producer.send(json.dumps(data).encode('utf-8'), partition_key=data["symbol"])
    print("Sending message", data)
    time.sleep(0.5)

client.close()
