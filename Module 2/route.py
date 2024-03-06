import pika
import random
import datetime
import json
import time

broker_host = "172.17.66.250"
broker_port = 5688

username = "admin"
password = "843427208034"
credentials = pika.PlainCredentials(username, password)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=broker_host, port=broker_port, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue="jaks_queue", durable=True)

routing_key = "iotdevice.*.tempsensor"

channel.queue_bind(exchange="jaks", queue="jaks_queue", routing_key=routing_key )

def lab_callback(ch, method, properties, body):
    output_routing_key = "alarm."+ str(method.routing_key) 
    message = json.loads(body.decode())
    if(message['temperature'] > 30):
        alarm_message = {
            "message": message,
            "alarm_type": "High Temperature"
        }
        alarm_message_string = json.dumps(alarm_message)
        ch.basic_publish(exchange = "jaks" , routing_key=output_routing_key, body=alarm_message_string)
        print("Saadetud alarm! Sõnum: %r" % body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue="jaks_queue", on_message_callback=lab_callback)
channel.start_consuming()