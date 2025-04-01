"""
Exclusive Consumer Example - Workshop CDC

This consumer uses the Exclusive subscription type, where only one
consumer can be active on the subscription at a time.
"""

from pulsar import Client, ConsumerType
import json

# Connect to Pulsar
client = Client('pulsar://localhost:6650')

# Subscribe with Exclusive type
consumer = client.subscribe(
    'persistent://public/default/tick',
    'exclusive-subscription',
    consumer_type=ConsumerType.Exclusive
)

print("Started EXCLUSIVE consumer")
print("Waiting for messages... (Press Ctrl+C to exit)")
print("Note: Try running a second instance of this consumer to see what happens!")

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
