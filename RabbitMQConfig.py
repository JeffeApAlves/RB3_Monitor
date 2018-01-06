# -*- coding: utf-8 -*-
"""
Created on Fri May 12 08:31:16 2017
@author: Jefferson
"""

import pika

class RabbitMQConfig(object):
    
  
    HOST = "localhost"
#    HOST = '192.168.0.114'
#    HOST = '192.168.42.12'
    USER = "senai"
    PW = "senai"
    VHOST = "/"
    PORT = 5672
 
    @staticmethod    
    def getConnectionParameters():    

        credentials = pika.PlainCredentials(RabbitMQConfig.USER, RabbitMQConfig.PW)
        params = pika.ConnectionParameters(RabbitMQConfig.HOST,RabbitMQConfig.PORT,RabbitMQConfig.VHOST,credentials,socket_timeout=1000,heartbeat_interval=200)
      
        return params
