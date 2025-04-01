"""
Key-Shared Consumer Example - Workshop CDC

This consumer uses the Key_Shared subscription type, where messages with
the same key are guaranteed to be delivered to the same consumer.
"""

from pulsar import Client, ConsumerType
import json

# Connect to Pulsar
client = Client('pulsar://localhost:6650')

# Subscribe with Key_Shared type
consumer = client.subscribe(
    'persistent://public/default/tick',
    'key-shared-subscription',
    consumer_type=ConsumerType.KeyShared
)

print("Started KEY_SHARED consumer")
print("Waiting for messages... (Press Ctrl+C to exit)")
print("Note: Start multiple instances and observe how messages with the same key (symbol)")
print("are always delivered to the same consumer instance!")

try:
    # Track symbols seen by this consumer
    symbols_seen = set()
    
    while True:
        # Wait for a message
        msg = consumer.receive()
        try:
            # Process the message
            data = msg.data().decode('utf-8')
            message = json.loads(data)
            
            # Track symbols for this consumer
            symbol = message.get('symbol')
            if symbol:
                symbols_seen.add(symbol)
            
            print(f"\nReceived message: {message}")
            print(f"Message ID: {msg.message_id()}")
            print(f"Symbols seen by this consumer: {symbols_seen}")
            
            # Acknowledge successful processing
            consumer.acknowledge(msg)
        except Exception as e:
            # Message failed to process
            print(f"Failed to process message: {e}")
            consumer.negative_acknowledge(msg)
            
except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    # Clean up
    consumer.close()
    client.close()
