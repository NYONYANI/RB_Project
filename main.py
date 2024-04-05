# 메인 파일 (main.py)

from function import *

# 로봇 IP 주소 및 포트 번호
robot_ip = '10.0.2.7'
command_port = 5000
data_port = 5001
# 전역 변수로 선언
global command_sock, data_sock

# 소켓 생성 및 연결
command_sock, data_sock = function.create_sockets(robot_ip, command_port, data_port)

# 연결 확인
check_connection()

# 원하는 함수 호출
#function.CobotInit(command_sock)
#function.MoveTCP(command_sock, 600,-300,800,0,0,0)
MoveJoint(0,10,10,0,10,10,1,1)
