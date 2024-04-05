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
    try:
        # TCP 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 로봇에 연결 시도
        result = sock.connect_ex((robot_ip, command_port))
        
        if result == 0:
            print('Connection successful')
        else:
            print('Connection failed')
        
        # 소켓 닫기
        sock.close()
        
    except Exception as e:
        print(f'Error checking connection: {e}')

# 연결 확인 예시
check_connection()