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

message = {
    "device_name": "jaks",
    "temperature": random.randint(20, 40),
    "time": str(datetime.datetime.now())
}

message_str = json.dumps(message)

my_routing_key = "iotdevice.jaks.tempsensor"


timer = 0
start_time = time.time()
try:
    while True:
        if time.time() - start_time < 5:
            continue
        message = {
            "device_name": "jaks",
            "temperature": random.randint(20, 40),
            "time": str(datetime.datetime.now())
        }
        message_str = json.dumps(message)
        print("Message:", message_str)
        channel.basic_publish(
            exchange="jaks",
            routing_key=my_routing_key,
            body=message_str)
        start_time = time.time()
except KeyboardInterrupt:
    print("Stopping publisher")

channel.close()
connection.close()