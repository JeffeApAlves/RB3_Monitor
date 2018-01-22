## Descrição

Publica mensagens com a telemetria da raspberry(Consumo de CPU,Memoria etc) na plataforma iot ThingSpeak o frontend é atualizado atrves de socket. Foi utilizado o framework Flask. 

![Thing Speak][thingspeak]

Abaixo segue a tela sendo atualizada via socket 

![web page][home_page]


## Instalação

1. Providenciar um ambiente python

2. Instalar dependênncias 


## Referências

[Websocket with Flask] [ref_flask]

[Tutorial raspberry as webserver][ref_rb]

[Introdução MQTT ][ref_mqtt]


[thingspeak]:images/thingspeak.png
[home_page]:images/web_page.png
[ref_flask]: https://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent
[ref_mqtt]:https://www.mathworks.com/help/thingspeak/mqtt-basics.html#zmw57dd0e21035
[ref_rb]:https://projects.raspberrypi.org/en/projects/python-web-server-with-flask/10