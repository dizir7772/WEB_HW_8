"""
Під час запуску скрипта producer.py він генерує певну кількість фейкових контактів та записує їх у базу даних.
Потім поміщає у чергу RabbitMQ повідомлення,
яке містить ObjectID створеного контакту, і так для всіх згенерованих контактів.
"""
from datetime import datetime
import json
import random

import pika
from faker import Faker
from models import Contacts


USERS_COUNT = 15
ways = ["email", "phone"]

fake = Faker('uk-UA')

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_email_queue', durable=True)
channel.queue_declare(queue='task_phone_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_email_queue')
channel.queue_bind(exchange='task_mock', queue='task_phone_queue')


# генерує певну кількість фейкових контактів та записує їх у базу даних
def contacts_seeds():
    for user in range(USERS_COUNT):
        contact = Contacts(
            fullname=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            prefer_way=random.choice(ways))
        contact.save()


def run_task(message, routing_key):
    channel.basic_publish(
        exchange='task_mock',
        routing_key=routing_key,
        body=json.dumps(message).encode(),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    print(" [x] Sent message to: %r" % message)


def send_message():
    contacts = Contacts.objects()
    for i, contact in enumerate(contacts, start=1):
        if str(contact.prefer_way) == "email":
            message = {
                "task": i,
                "id": str(contact.id),
                "email": contact.email,
                "date": datetime.now().isoformat()
            }
            routing_key = 'task_email_queue'
            run_task(message, routing_key)

        elif str(contact.prefer_way) == "phone":
            message = {
                "task": i,
                "id": str(contact.id),
                "phone": contact.phone,
                "date": datetime.now().isoformat()
            }
            routing_key = 'task_phone_queue'
            run_task(message, routing_key)


if __name__ == '__main__':
    contacts_seeds()
    send_message()
    connection.close()
