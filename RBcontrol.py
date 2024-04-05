import socket

# 로봇의 IP 주소와 포트 번호
robot_ip = '10.0.2.7'
command_port = 5000
data_port = 5001

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
    print("Try connect...")
    try:
        # 로봇으로부터 데이터 수신 시도
        data = command_sock.recv(1)

        # 데이터 수신 성공 시 연결 성공
        if data:
            print('Connection successful')
            return True

        # 데이터 수신 실패 시 연결 실패
        else:
            print('Connection failed')
            return False

    except Exception as e:
        print(f'Error checking connection: {e}')
        return False

def CobotInit():
    send_command("mc jall init")

def MoveJoint( joint1, joint2,joint3,joint4,joint5, joint6,spd = -1, acc = -1):
    send_command(f"jointall {spd}, {acc}, {joint1}, {joint2}, {joint3}, {joint4}, {joint5}, {joint6}")

# 연결 확인 예시

def MoveTCP(x,y,z,rx,ry,rz,spd = -1, acc = -1):
    print(f"movetcp {spd}, {acc}, {x}, {y}, {z}, {rx}, {ry}, {rz}")
    send_command(f"movetcp {spd}, {acc}, {x}, {y}, {z}, {rx}, {ry}, {rz}")

if __name__ == "__main__":
    CobotInit()
    MoveTCP(300,300,300,0,0,0)
    #check_connection()






