from __future__ import print_function
from threading import Thread
import time
import thingspeak
from ast import literal_eval
import os
import json
from thingspeak_config import thingspeak_config

class Subscribe (object):

    def __init__(self):
        self._temperature = ''
        self._cpu =''
        self._memory =''
        self._disk=''
        self._pressure =''
        self._humidity =''
        self._ts_channel = None

    def start(self):
        self.ts_channel = thingspeak.Channel(thingspeak_config.CHANNEL_ID, thingspeak_config.READ_API_KEY)

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self,value):
        self._temperature = value

    @property
    def cpu(self):
        return self._cpu

    @cpu.setter
    def cpu(self,value):
        self._cpu = value

    @property
    def memory(self):
        return self._memory

    @memory.setter
    def memory(self,value):
        self._memory = value

    @property
    def disk(self):
        return self._disk

    @disk.setter
    def disk(self,value):
        self._disk = value

    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    def pressure(self,value):
        self._pressure = value

    @property
    def humidity(self):
        return self._humidity

    @humidity.setter
    def humidity(self,value):
        self._humidity = value

    def readValue(self,id):
        data = json.loads(self.ts_channel.get_field_last(field=id))
        return data['field'+id]

    def readValues(self):

        self.temperature = self.readValue('1')
        self.disk = self.readValue('2')
        self.cpu = self.readValue('3')
        self.memory = self.readValue('4')
        self.pressure = self.readValue('5')
        self.humidity = self.readValue('6')
