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

channel.queue_declare(queue="jaks_alarm_queue", durable=True)

routing_key = "alarm.#"

channel.queue_bind(exchange="jaks", queue="jaks_alarm_queue", routing_key=routing_key )

def lab_callback(ch, method, properties, body):
    print("Saabunud sõnum: %r" % body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue="jaks_alarm_queue", on_message_callback=lab_callback)
channel.start_consuming()