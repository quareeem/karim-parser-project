import pika

def send_rabbit(json_data):
    credentials = pika.PlainCredentials('kara','qwerty')
    params = pika.ConnectionParameters(
        host='rabbitmq', 
        credentials=credentials, 
        connection_attempts=3, 
        retry_delay=10
    )
    connection = pika.BlockingConnection(params)
        
    channel = connection.channel()

    # channel.queue_declare(queue='testque')

    channel.exchange_declare(exchange='exc_shopkz', exchange_type='fanout')

    channel.basic_publish(exchange='exc_shopkz', routing_key='', body=json_data)
    print(" [x] Sent  json_data")

    connection.close()







    # channel.exchange_declare('test', durable=True, exchange_type='topic')
    # channel.queue_declare(queue= 'A')
    # channel.queue_bind(exchange='test', queue='A', routing_key='A')
    # channel.queue_declare(queue= 'B')
    # channel.queue_bind(exchange='test', queue='B', routing_key='B')
    # channel.queue_declare(queue= 'C')
    # channel.queue_bind(exchange='test', queue='C', routing_key='C')#messaging to queue named C
    # message= 'hello consumer!!!!!'
    # channel.basic_publish(exchange='test', routing_key='C', body= message)
    # channel.close()








# credentials = pika.PlainCredentials('kara','qwerty')
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=credentials))

# channel.exchange_declare('test', durable=True, exchange_type='topic')
# channel.queue_declare(queue= 'A')
# channel.queue_bind(exchange='test', queue='A', routing_key='A')
# channel.queue_declare(queue= 'B')
# channel.queue_bind(exchange='test', queue='B', routing_key='B')
# channel.queue_declare(queue= 'C')
# channel.queue_bind(exchange='test', queue='C', routing_key='C')#messaging to queue named C
# message= 'hello consumer!!!!!'
# channel.basic_publish(exchange='test', routing_key='C', body= message)
# channel.close()