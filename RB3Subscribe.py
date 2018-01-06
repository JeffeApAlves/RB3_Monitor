from __future__ import print_function
from threading import Thread
import paho.mqtt.client as mqtt
import time
import thingspeak
from ast import literal_eval
import os
import json

# ID do canal do ThingSpeak
CHANNEL_ID = "315831"

# Chave de escrita da API para o canal
READ_API_KEY = "TF63H3V6I2UWO954"

#Host
mqttHost = "mqtt.thingspeak.com"

#Camada Transporte
tTransport = "websockets"

UPDATE_INTERVAL = 5

#Porta 
tPort = 80

#class RB3Subscribe (Thread):
class RB3Subscribe (object):
    
    def __init__(self):
        #Thread.__init__(self)
        # Criaca do topico
        #self.topic = "channels/" + channelID + "/publish/" + apiKey
        self.temperature = ''
        self.cpu =''
        self.memory =''
        self.disk=''
        self.pressure =''
        self.humidity =''
        self.ts_channel = None

    def init(self):
        self.ts_channel = thingspeak.Channel(CHANNEL_ID, READ_API_KEY)
        self.client = mqtt.Client()
        self.client.connect(mqttHost,tPort)
        self.client.loop_start()
#        Thread.start()
 
    def getCPUtemperature(self):
        return self.temperature
  
    def getCPU(self):
        return self.cpu

    def getMemory(self):
        return self.memory

    def getDisk(self):
         return self.disk

    def getPressure(self):
        return self.pressure

    def getHumidity(self):
        return self.humidity

    def readValue(self,id):
        data = json.loads(self.ts_channel.get_field_last(field=id))
        return data['field'+id]

    def readValues(self):
        
        data = json.loads(self.ts_channel.get_field_last(field='1'))

        self.temperature = self.readValue('1')
        self.disk = self.readValue('2')
        self.cpu = self.readValue('3')
        self.memory = self.readValue('4')
        self.pressure = self.readValue('5')
        self.humidity = self.readValue('6')
        
#    def run(self):
#
#        self.client.loop_start()
#        
#        while(1):
#            self.readValues()
#            time.sleep(UPDATE_INTERVAL)
