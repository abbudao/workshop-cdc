"""
Failover Consumer Example - Workshop CDC

This consumer uses the Failover subscription type, where consumers have
a priority order and the highest priority consumer receives all messages.
If the active consumer disconnects, the next highest priority takes over.
"""

from pulsar import Client, ConsumerType
import json

# Connect to Pulsar
client = Client('pulsar://localhost:6650')

# Subscribe with Failover type
consumer = client.subscribe(
    'persistent://public/default/tick',
    'failover-subscription',
    consumer_type=ConsumerType.Failover
)

print("Started FAILOVER consumer")
print("Waiting for messages... (Press Ctrl+C to exit)")
print("Note: Start multiple instances of this consumer and kill the primary to see failover!")

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
