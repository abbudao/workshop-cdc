"""
Shared Consumer Example - Workshop CDC

This consumer uses the Shared subscription type, where multiple consumers
can process messages from the same topic in a round-robin fashion.
"""

from pulsar import Client, ConsumerType
import json

# Connect to Pulsar
client = Client('pulsar://localhost:6650')

# Subscribe with Shared type
consumer = client.subscribe(
    'persistent://public/default/tick',
    'shared-subscription',
    consumer_type=ConsumerType.Shared
)

print("Started SHARED consumer")
print("Waiting for messages... (Press Ctrl+C to exit)")
print("Note: Start multiple instances to see how messages are distributed!")

try:
    while True:
        # Wait for a message
        msg = consumer.receive()
        try:
            # Process the message
            data = msg.data().decode('utf-8')
            message = json.loads(data)
            
            print(f"\nReceived message: {message}")
            print(f"Message ID: {msg.message_id()}")
            
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
