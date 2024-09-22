import pika
import json
import allure
from allure import step


@step("Send a message to RabbitMQ queue")
def send_message(queue_name, message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)

        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            ))

        allure.step(f"Sent message to {queue_name}: {message}")
    except Exception as e:
        allure.step(f"Error sending message: {e}")
        raise
    finally:
        connection.close()


@step("Receive message from RabbitMQ queue")
def receive_message(queue_name):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)

        method_frame, header_frame, body = channel.basic_get(queue_name)
        if method_frame:
            message = json.loads(body)
            allure.step(f"Received message from {queue_name}: {message}")
            return message
        else:
            allure.step("No message received")
            return None
    except Exception as e:
        allure.step(f"Error receiving message: {e}")
        raise
    finally:
        connection.close()
