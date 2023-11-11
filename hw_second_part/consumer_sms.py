"""
Скрипт consumer.py отримує з черги RabbitMQ повідомлення,
обробляє його та імітує функцією-заглушкою надсилання повідомлення по email.
Після надсилання повідомлення необхідно логічне поле для контакту встановити в True.
Скрипт працює постійно в очікуванні повідомлень з RabbitMQ.
"""

import json
import pika
from models import Contacts


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='task_phone_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    print(f" [x] Received {message}")

    contact = Contacts.objects(id=message.get('id'))
    contact.update(is_delivered=True)

    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_phone_queue', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()