from __future__ import print_function
from threading import Thread
import paho.mqtt.publish as publish
import os
import psutil
from thingspeak_config import thingspeak_config
#from sense_emu import SenseHat

class RB3Publish (Thread):

    #sense = SenseHat()

    def __init__(self):

        Thread.__init__(self)
        # Criaca do topico
        self.topic = "channels/" + thingspeak_config.CHANNEL_ID + "/publish/" + thingspeak_config.APIKEY

    @property
    def temperature(self):
        res = os.popen('sudo vcgencmd measure_temp').readline()
        return(res.replace("temp=","").replace("'C\n",""))

    @property
    def cpu(self):
        return psutil.cpu_percent(interval=5)

    @property
    def memory(self):
        return psutil.virtual_memory().percent

    @property
    def disk(self):
        disk = psutil.disk_usage('/')
        # Divide from Bytes -> KB -> MB -> GB
        free = round(disk.free/1024.0/1024.0/1024.0,1)
        total = round(disk.total/1024.0/1024.0/1024.0,1)
        return total

    @property
    def pressure(self):
        return 0.0
	#return self.sense.pressure

    @property
    def humidity(self):
        return 0.0
	#return self.sense.humidity

    def run(self):

        while(1):

            # Constroi o payload
            payload = "field1=%s&field2=%d&field3=%d&field4=%d&field5=%d&field6=%d" % (self.temperature,self.disk,self.cpu,self.memory,self.pressure,self.humidity)

            # Tenta publicar
            try:
                publish.single(self.topic, payload, hostname=thingspeak_config.mqttHost, transport=thingspeak_config.tTransport, port=thingspeak_config.tPort)
                print ("Publiacado no ThingSpeak=" + payload)

            except (KeyboardInterrupt):
                break

            except:
                print ("Algum erro ocorreu durante a publicacao da informacao")
