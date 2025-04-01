"""
CDC Event Consumer - Workshop CDC

This consumer listens for CDC events from Debezium that are published to Pulsar.
It's designed to receive events from the Outbox pattern implementation.
"""

from pulsar import Client, ConsumerType
import json
import re

# Connect to Pulsar
client = Client('pulsar://localhost:6650')

# Subscribe to CDC events (using regex to match all event topics)
consumer = client.subscribe(
    re.compile(r'persistent://public/default/workshop\.event\..*'),
    'cdc-subscription',
    consumer_type=ConsumerType.Shared
)

print("Started CDC Event Consumer")
print("Listening for database events... (Press Ctrl+C to exit)")
print("Tip: Insert records into the events table to see CDC in action")

try:
    while True:
        # Wait for a message
        msg = consumer.receive()
        try:
            # Process the message
            data = msg.data().decode('utf-8')
            event_data = json.loads(data)
            
            # Display event information
            print("\n" + "="*60)
            print(f"Received CDC Event on topic: {msg.topic_name()}")
            print(f"Message ID: {msg.message_id()}")
            print("-"*60)
            
            # Pretty print the event data
            print("Event Data:")
            print(json.dumps(event_data, indent=2))
            print("="*60)
            
            # Acknowledge successful processing
            consumer.acknowledge(msg)
        except Exception as e:
            # Message failed to process
            print(f"Failed to process CDC event: {e}")
            consumer.negative_acknowledge(msg)
            
except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    # Clean up
    consumer.close()
    client.close()
