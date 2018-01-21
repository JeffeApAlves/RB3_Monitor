import pika
import sys
import time
from random import randint,uniform
from RabbitMQConfig import RabbitMQConfig

QUEUE_TLM = 'TLM00002'
EXCHANGE_TLM = 'TLM'
ROUTING_KEY = 'tlm.00002'
HOST = 'localhost'
PORT =  5672

FRAME_HEADER = "{0:08}:{1:08}:{2:010.0f}:{3:2}:{4:3}:{5:03}:"
FRAME_PAYLOAD = "{0}:{1}:{2}:{3}:{4}:{5}:{6}:{7}:{8}:{9}:{10}:{11:10.0f}"

class kl25z (object):

    def __init__(self):
        print("Iniciando conexão com o message broker...")
        #self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
        self.connection = pika.BlockingConnection(parameters=RabbitMQConfig.getConnectionParameters())
        self.channel    = self.connection.channel()

    def init(self):
        print("Criando Exchanges")
        self.createExchanges()
        print("Criando Queues")
        self.createQueues()
        print("Criando Binds")
        self.createBinds()

    def createExchanges(self):
        self.channel.exchange_declare(exchange=EXCHANGE_TLM,exchange_type='direct')

    def createBinds(self):
        self.channel.queue_bind(exchange=EXCHANGE_TLM,
                           queue=QUEUE_TLM,
                           routing_key=ROUTING_KEY)

    def createQueues(self):
        self.channel.queue_declare(queue = QUEUE_TLM , durable = True)

    def publishTLM(self):
        payload = self.createPayLoad()
        self.channel.basic_publish(  exchange=EXCHANGE_TLM,
                                routing_key=ROUTING_KEY,
                                body=payload)
    def deInit(self):
        self.connection.close()

    def createPayLoad(self):
        payload = FRAME_PAYLOAD.format( -23.591387,
                                        -46.645126,
                                        randint(3500,4000),
                                        randint(1000,1500),
                                        randint(2000,3000),
                                        uniform(0.1,0.2),
                                        uniform(0.0,0.1),
                                        uniform(0.9,1.2),
                                        randint(40,120),
                                        randint(800,830),
                                        1,
                                        time.time())

        header = FRAME_HEADER.format(2,1,time.time(),"AN","TLM",len(payload))
        print("Frame: "+header + payload)
        return header + payload
