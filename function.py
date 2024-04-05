import socket

# TCP 소켓 생성
def create_sockets(robot_ip, command_port, data_port):
    command_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    command_sock.connect((robot_ip, command_port))
    data_sock.connect((robot_ip, data_port))
    return command_sock, data_sock

# 로봇에게 명령을 전송하는 함수
def send_command(command_sock, command):
    try:
        command_sock.sendall(command.encode())
    except Exception as e:
        print(f'Error sending command: {e}')

# 데이터를 수신하는 함수
def receive_data(data_sock):
    try:
        data = data_sock.recv(1024)
        print(f'Received data: {data.decode()}')
    except Exception as e:
        print(f'Error receiving data: {e}')

# 연결 확인 함수
def check_connection(robot_ip, command_port):
    try:
        # 이미 연결된 소켓 사용하여 확인
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((robot_ip, command_port))
        print('Connection successful')
    except Exception as e:
        print(f'Connection failed: {e}')

# Cobot 초기화 함수
def CobotInit():
    send_command( "mc jall init")

# TCP 좌표 이동 함수
def MoveTCP( x, y, z, rx, ry, rz, spd=-1, acc=-1):
    send_command( f"movetcp {spd}, {acc}, {x}, {y}, {z}, {rx}, {ry}, {rz}")

# 관절 좌표 이동 함수
def MoveJoint( joint1, joint2, joint3, joint4, joint5, joint6, spd=-1, acc=-1):
    send_command( f"jointall {spd}, {acc}, {joint1}, {joint2}, {joint3}, {joint4}, {joint5}, {joint6}")
