import paho.mqtt.client as mqtt
import os
from datetime import datetime

# 설정
BROKER = "192.168.100.133"
PORT = 1883
SAVE_DIR = "captured_images"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def on_connect(client, userdata, flags, rc):
    print(f"[+] 브로커 연결 성공: {BROKER}:{PORT}")
    # 모든 토픽 구독 (와일드카드 #)
    client.subscribe("#")
    print("[+] 모든 토픽 구독 시작 (#)")

def on_message(client, userdata, msg):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = f"{SAVE_DIR}/image_{timestamp}.jpg"
        
        # 페이로드 크기 확인 (이미지 데이터라고 가정)
        if len(msg.payload) > 1000:
            with open(filename, "wb") as f:
                f.write(msg.payload)
            
            print(f"[*] 메시지 수신!")
            print(f"    토픽: {msg.topic}")
            print(f"    크기: {len(msg.payload)} bytes")
            print(f"    [저장됨] {filename}")
    except Exception as e:
        print(f"[-] Error processing message: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("[*] Sniffer Starting...")
client.connect(BROKER, PORT, 60)
client.loop_forever()
