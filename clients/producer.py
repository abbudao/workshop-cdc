"""
Simple Stock Ticker Producer - Workshop CDC

This producer sends simulated stock price data to a Pulsar topic.
Each message has a symbol (stock ticker) and a random price.
"""

import pulsar
import json
import time
import random

# Available stock symbols
SYMBOLS = ["AAPL", "MSFT", "GOOG", "AMZN", "META", "TSLA", "PETR4", "VALE3"]

# Connect to Pulsar
client = pulsar.Client("pulsar://localhost:6650")

# Create a producer
producer = client.create_producer("persistent://public/default/tick")

print("Started stock ticker producer")
print("Sending messages every 0.5 seconds... (Press Ctrl+C to exit)")

try:
    message_count = 0
    
    while True:
        # Create a random stock tick
        symbol = random.choice(SYMBOLS)
        price = round(random.uniform(10, 1000), 2)
        
        # Create message data
        data = {
            "symbol": symbol,
            "price": price,
            "timestamp": int(time.time())
        }
        
        # Convert to JSON and send
        json_data = json.dumps(data)
        producer.send(json_data.encode('utf-8'), partition_key=symbol)
        
        # Print status
        message_count += 1
        print(f"Sent message #{message_count}: {data}")
        
        # Wait before sending next message
        time.sleep(0.5)
        
except KeyboardInterrupt:
    print("\nShutting down producer...")
finally:
    # Clean up
    producer.close()
    client.close()
