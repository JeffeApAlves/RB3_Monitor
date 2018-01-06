import pika
import json
from threading import Thread
import time

HOST = '192.168.0.114'
PORT =  5672

ADDRESS = 2
CMD_EXCHANGE = 'cmd'
ANS_EXCHANGE = 'ans'

CMD_QUEUE = "cmd{0:d}"
ANS_QUEUE = "ans{0:d}"

ANS_ROUTE = "ans{0:d}"

connection = None
channel = None
UPDATE_INTERVAL = 5

class Telemetria (Thread):

    def __init__(self):
        Thread.__init__(self)

    def close(self):
        connection.close()
    
    def open(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(HOST))
        channel = connection.channel()

    def declareQueue(self):
        channel.queue_declare(queue=CMD_QUEUE.format(ADDRESS))

    def publishAns(self,frame):
        channel.basic_publish(exchange = ANS_QUEUE.format(ADDRESS),
                      routing_key= ANS_QUEUE.format(ADDRESS),
                      body=frame)

    def createConsume(self,):
        channel.basic_consume(callbackCMD,
                      queue=CMD_QUEUE,
                      no_ack=True)

    def callbackCMD(self,ch, method, properties, body):
        print(" [x] Received %r" % body)

    def run(self):
        channel.start_consuming()

        while(1):
            publishAns(self,"00002:00001")
            time.sleep(UPDATE_INTERVAL)
