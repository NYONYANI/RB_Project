#function.py를 import 해서 사용하는데 앞에 이름 붙히지 않고 쓰게 해줘
import socket
from function import *


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


if __name__ == "__main__":
    #CobotInit()
    #MoveTCP(600,-300,800,0,0,0)
    MoveJoint(0,10,10,0,10,10,1,1)
    #check_connection()
    





