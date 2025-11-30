import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw
import io
import datetime
import time

# 상황에 맞게
broker = "192.168.100.133"
topic = "iot/image"

client = mqtt.Client()
client.connect(broker, 1883, 60)

while True:
    # 이미지 생성
    img = Image.new("RGB", (640, 480), (0, 128, 255))
    draw = ImageDraw.Draw(img)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((20, 20), "IoT Camera", fill=(255, 255, 255))
    draw.text((20, 60), timestamp, fill=(255, 255, 255))

    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    img_bytes = buf.getvalue()

    client.publish(topic, img_bytes)
    print(f"[전송됨] {timestamp}, 크기: {len(img_bytes)} bytes")

    time.sleep(5)
