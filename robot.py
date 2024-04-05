import socket

def send_command(sock, command):
    try:
        print(command.encode())
        sock.sendall(command.encode())
    except Exception as e:
        print(f'Error sending command: {e}')

def receive_data(sock):
    try:
        data = sock.recv(1024)
        print(f'Received data: {data.decode()}')
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
    send_command(sock, f"movetcp {spd}, {acc}, {x}, {y}, {z}, {rx}, {ry}, {rz}")