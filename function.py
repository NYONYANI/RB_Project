#import socket

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