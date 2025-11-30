import paho.mqtt.client as mqtt
import os
import datetime

BROKER = "192.168.100.132"     
TOPIC = "iot/image"
SAVE_DIR = "/home/ksm/iot_images"

os.makedirs(SAVE_DIR, exist_ok=True)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, message):
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{SAVE_DIR}/image_{now}.jpg"

    try:
        with open(filename, "wb") as f:
            f.write(message.payload)

        print(f"이미지 저장 완료 → {filename}")

    except Exception as e:
        print("이미지 저장 실패:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_forever()
