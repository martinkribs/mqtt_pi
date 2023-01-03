import os
import signal
import sys
import time
import json

import paho.mqtt.client as mqtt
import config
import colorlight


def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('lights')
    else:
        print('Bad connection. Code:', rc)


def on_message(mqtt_client, userdata, msg):
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
    light = json.loads(msg.payload)
    if light.name == config.NAME and light.topic == config.MQTT_TOPIC_BASE:
        colorlight.Led.start()


def signal_handler(frame):
    # "logoff" before disconnect
    mqtt.disconnect()
    time.sleep(2)
    sys.exit(0)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(config.MQTT_USER, config.MQTT_PASSWORD)
client.connect(
    host=config.MQTT_SERVER,
    port=config.MQTT_PORT,
    keepalive=config.MQTT_KEEPALIVE
)
client.loop_start()

print('Press Ctrl+C to quit')
if sys.platform == 'linux':
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
else:
    os.system("pause")
