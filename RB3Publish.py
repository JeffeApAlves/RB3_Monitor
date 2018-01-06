from __future__ import print_function
from threading import Thread
import paho.mqtt.publish as publish
import os
from sense_emu import SenseHat
import psutil

# ID do canal do ThingSpeak
channelID = "315831"

# Chave de escrita da API para o canal
apiKey = "IXKST4CB6ZSZP1FA"

#Host
mqttHost = "mqtt.thingspeak.com"

#Camada Transporte
tTransport = "websockets"

#Porta 
tPort = 80


class RB3Publish (Thread):

    sense = SenseHat()
   
    def __init__(self):

        Thread.__init__(self)
        # Criaca do topico
        self.topic = "channels/" + channelID + "/publish/" + apiKey
        

    def getCPUtemperature(self):
        res = os.popen('vcgencmd measure_temp').readline()
        return(res.replace("temp=","").replace("'C\n",""))

    def getCPU(self):
        return psutil.cpu_percent(interval=5)

    def getMemory(self):
        return psutil.virtual_memory().percent

    def getDisk(self):
        disk = psutil.disk_usage('/')
        # Divide from Bytes -> KB -> MB -> GB
        free = round(disk.free/1024.0/1024.0/1024.0,1)
        total = round(disk.total/1024.0/1024.0/1024.0,1)
        return total

    def getPressure(self):
        return self.sense.pressure

    def getHumidity(self):
        return self.sense.humidity
        
    def run(self):
        
        while(1):
    
            #Coleta estatisiticas do sistema
            cpu = self.getCPU()
            ram = self.getMemory()            
            disk = self.getDisk()
            temperature = self.getCPUtemperature()
            pressure = self.getPressure()
            humidity = self.getHumidity()
            
            #Constroi o payload
            payload = "field1=" + temperature + "&field2=" + str(disk) + "&field3=" + str(cpu) + "&field4=" + str(ram) + "&field5=" + str(pressure) + "&field6=" + str(humidity)

            # Tenta publicar 
            try:
                publish.single(self.topic, payload, hostname=mqttHost, transport=tTransport, port=tPort)
                print ("Publiacado no ThingSpeak=" + payload)

            except (KeyboardInterrupt):
                break

            except:
                print ("Algum erro ocorreu durante a publicacao da informacao")

