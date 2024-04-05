# 메인 파일 (main.py)

from function import *


import time
import pywifi
from pywifi import const

def connect_to_wifi(ssid):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # 첫 번째 인터페이스를 사용합니다.

    # 스캔
    iface.scan()
    time.sleep(1)
    scan_results = iface.scan_results()
    
    # 스캔된 와이파이 목록 출력
    # print("스캔된 와이파이 목록:")
    # for result in scan_results:
    #     print(result.ssid)

    # 주어진 SSID를 찾아 연결
    for result in scan_results:
        if result.ssid == ssid:
            profile = pywifi.Profile()
            profile.ssid = ssid
            profile.auth = const.AUTH_ALG_OPEN  # 오픈 인증 사용
            profile.akm.append(const.AKM_TYPE_NONE)  # 암호화 없음
            profile.auth = const.AUTH_ALG_OPEN

            # 연결 시도
            iface.remove_all_network_profiles()  # 이전 프로필 제거
            tmp_profile = iface.add_network_profile(profile)
            iface.connect(tmp_profile)
            time.sleep(5)  # 연결 시간을 기다립니다.
            
            if iface.status() == const.IFACE_CONNECTED:  # 연결 상태 확인
                print(f"와이파이 '{ssid}'에 연결되었습니다.")
                return True
            else:
                print("와이파이 연결에 실패했습니다.")
                return False

    print(f"와이파이 '{ssid}'를 찾을 수 없습니다.")
    return False

# 와이파이 이름
wifi_ssid = "RB5-850"
connect_to_wifi(wifi_ssid)

# 로봇 IP 주소 및 포트 번호
robot_ip = '10.0.2.7'
command_port = 5000
data_port = 5001
# 전역 변수로 선언

# TCP 소켓 생성
command_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 로봇에 연결
command_sock.connect((robot_ip, command_port))
data_sock.connect((robot_ip, data_port))

# 로봇에게 명령을 전송하는 함수
def send_command(command):
    try:
        # 명령 전송
        print(command.encode())
        command_sock.sendall(command.encode())
    except Exception as e:
        print(f'Error sending command: {e}')

# 데이터를 수신하는 함수
def receive_data():
    try:
        # 데이터 수신
        data = data_sock.recv(1024)
        
        # 수신한 데이터 처리
        # TODO: 데이터 처리 로직을 구현하세요.
        print(f'Received data: {data.decode()}')
        
    except Exception as e:
        print(f'Error receiving data: {e}')

# 연결 확인 함수
def check_connection():
    try:
        # 이미 연결된 소켓 사용하여 확인
        command_sock.getpeername()
        print('Connection successful')
    except Exception as e:
        print(f'Connection failed: {e}')


def CobotInit():
    send_command("mc jall init")

def MoveJoint( joint1, joint2,joint3,joint4,joint5, joint6,spd = -1, acc = -1):
    send_command(f"jointall {spd}, {acc}, {joint1}, {joint2}, {joint3}, {joint4}, {joint5}, {joint6}")

# 연결 확인 예시

def MoveTCP(x,y,z,rx,ry,rz,spd = -1, acc = -1):
    print(f"movetcp {spd}, {acc}, {x}, {y}, {z}, {rx}, {ry}, {rz}")
    send_command(f"movetcp {spd}, {acc}, {x}, {y}, {z}, {rx}, {ry}, {rz}")

if __name__ == "__main__":
    #CobotInit()
    #MoveTCP(600,-300,800,0,0,0)
    MoveJoint(0,10,10,0,10,10,1,1)
    #check_connection()
    
