import pika, sys, os, json
from db_operations import insert_into_table

all_received_data = []


def main():
    credentials = pika.PlainCredentials('kara','mara')
    params = pika.ConnectionParameters(
        host='rabbitmq', 
        credentials=credentials, 
        connection_attempts=3, 
        retry_delay=10
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.exchange_declare(exchange='shopkz_exchange', exchange_type='direct')
    queue = channel.queue_declare(queue='', exclusive=True)
    channel.queue_bind(
        exchange='shopkz_exchange', 
        queue=queue.method.queue,
        routing_key='shopkz_key'
    )

    def callback(ch, method, properties, body):
        print(f" [x] Received {type(body)}")
        data_str = body
        data_json = json.loads(data_str) 
        print('- - - - r e c e i v e d - - - -')
        table_name = next(k for k in data_json.keys())
        insert_into_table(data_json, table_name)

    channel.basic_consume(queue=queue.method.queue, on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
