
import reqdata

import socket

def send_command(sock, command):
    try:
        print(command.encode())
        sock.sendall(command.encode())
    except Exception as e:
        print(f'Error sending command: {e}')

import struct

def Receive_data(sock):
    try:
        send_command(sock, "reqdata")
        receive_data = sock.recv(1024)  # The total size of the structure
        robot_state.unpack(receive_data)
        #print(robot_state.jnt_ref)
    except Exception as e:
        print(f'Error receiving data: {e}')



def check_connection(sock):
    try:
        sock.getpeername()
        print('Connection successful')
    except Exception as e:
        print(f'Connection failed: {e}')

def CobotInit(sock):
    send_command(sock, "mc jall init")

def MoveJoint(sock, joint1, joint2, joint3, joint4, joint5, joint6, spd = -1, acc = -1):
    send_command(sock, f"jointall {spd}, {acc}, {joint1}, {joint2}, {joint3}, {joint4}, {joint5}, {joint6}")

def MoveTCP(sock, x, y, z, rx, ry, rz, spd = -1, acc = -1):
    while robot_state.robot_state != 0:
        receive_data()
    send_command(sock, f"movetcp {spd}, {acc}, {x}, {y}, {z}, {rx}, {ry}, {rz}")
#tool 작동 코드 전압, d0, d1 로 구성
def Tool(sock, voltage, d0, d1):
    send_command(sock, f"tool_out {voltage}, {d0}, {d1}")

#reqdata 문자열을 보내면 5001포트로 데이터가 수신되는 코드
def ReqData(sock,data_sock):
    Receive_data(data_sock)    

def pgmode_real(sock):
    send_command(sock,f"pgmode real")



robot_state = reqdata.RobotData()