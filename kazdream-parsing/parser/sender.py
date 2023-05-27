import pika
import os
import json
import pika
from dotenv import load_dotenv


load_dotenv()
rab_username = os.environ['RABBITMQ_USERNAME']
rab_password = os.environ['RABBITMQ_PASSWORD']


def send_rabbit(json_data):
    credentials = pika.PlainCredentials(username=rab_username, password=rab_password)
    params = pika.ConnectionParameters(
        host='rabbitmq', 
        credentials=credentials, 
        connection_attempts=3, 
        retry_delay=10
    )

    connection = pika.BlockingConnection(parameters=params)
    channel = connection.channel()

    channel.basic_publish(exchange='shopkz_exchange', routing_key='shopkz_key', body=json_data)
    print(" [x] Sent  json_data")
    connection.close()
