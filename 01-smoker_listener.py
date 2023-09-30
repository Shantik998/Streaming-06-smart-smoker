"""
    This program listens and consumes messages from bbq_producer_smoker
    for the temperature of the smoker every 30 seconds. It also sends 
    an alert if in a 2.5 minute period the smoker goes down by more than 
    15 degrees in temperature. 

    Shanti Kandel 
    09/28/2023

"""

import pika
import sys
import time
from collections import deque

s_deque = deque(maxlen=5)
alert = "Alert! Alert! Alert! Smoker temperature is decreasing at a high rate! Temperature has gone down by more than 15 degrees in 2.5 minutes"


# Define a callback function to be called when a message is received
def smoker_callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # Splitting the smoker data to isolate the temperature
    smoker_message = body.decode().split(",")
    
    if len(smoker_message) >= 2:
        try:
            # Convert the temperature string to a float
            temp = float(smoker_message[1])
            # Place the temperature data in the right side of the deque
            s_deque.append(temp)
            
            # Create the alert if the deque is full
            if len(s_deque) == 5:
                smokeralert = s_deque[0] - s_deque[4]
                if smokeralert > 15:
                    print(alert)
            
            # Print the received temperature
            print(f" [x] Received the temperature. Smoker temperature is {temp} degrees")
        
        except ValueError:
            print("Invalid temperature value received.")
    else:
        print("Invalid message format received.")
    
    # Acknowledge the message was received and processed
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Define a main function to run the program
def main(hn: str = "localhost", qn: str = "task_queue"):
    """ Continuously listen for task messages on a named queue."""
    
    # When a statement can go wrong, use a try-except block
    try:
        # Try this code, if it works, keep going
        # Create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))
    
    # Except, if there's an error, do this
    except Exception as e:
        print()
        print("ERROR: Connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:
        # Use the connection to create a communication channel
        channel = connection.channel()

        # Use the channel to declare a durable queue
        # A durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # Messages will not be deleted until the consumer acknowledges
        channel.queue_declare(queue=qn, durable=True)

        # Configure the channel to listen on a specific queue,
        # use the callback function named callback,
        # and do not auto-acknowledge the message (let the callback handle it)
        channel.basic_consume(queue=qn, auto_ack=False, on_message_callback=smoker_callback)

        # Print a message to the console for the user
        print(" [*] Ready for work. To exit press CTRL+C")

        # Start consuming messages via the communication channel
        channel.start_consuming()

    # Except, in the event of an error OR user stops the process, do this
    except Exception as e:
        print()
        print("ERROR: Something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print("User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()


# Standard Python idiom to indicate the main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # Call the main function with the information needed
    main("localhost", "01-smoker")
