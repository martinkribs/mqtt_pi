import os
import signal
import sys
import time
import json

import paho.mqtt.client as mqtt
import config
import colorlight


# on successfully connection
def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('lights')
    else:
        print('Bad connection. Code:', rc)


# on message
def on_message(mqtt_client, userdata, msg):
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
    light = json.loads(msg.payload)
    if light['name'] == config.NAME and msg.topic == config.MQTT_TOPIC_BASE:
        r, g, b = hex_to_rgb(light['colour'])
        colorlight.Led.change(led, r, g, b)
        status = colorlight.Led.get_status(led)
        colour = rgb_to_hex(colorlight.Led.get_color(led))
        brightness = colorlight.Led.get_brightness(led)
        data = {'name': config.NAME, 'status': status, 'colour': colour,
                'brightness': brightness}
        mqtt.Client.publish(client, config.MQTT_TOPIC_BASE, json.dumps(data))


# log off handler
def signal_handler():
    # "logoff" before disconnect
    mqtt.Client.disconnect(client)
    time.sleep(2)
    sys.exit(0)


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


# Light
led = colorlight.Led()
colorlight.Led.start(led)

# MQTT
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
