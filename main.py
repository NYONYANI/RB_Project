from wifi import connect_to_wifi
from robot import *

if __name__ == "__main__":
    wifi_ssid = "RB5-850"
    connect_to_wifi(wifi_ssid)

    robot_ip = '10.0.2.7'
    command_port = 5000
    data_port = 5001

    command_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    command_sock.connect((robot_ip, command_port))
    data_sock.connect((robot_ip, data_port))

    #사용 가능한 명령어를 출력
    print("Available commands: Movej, Movel, tool, reqdata, exit")

    while True:
        command = input("Enter command: ")
        if command == "exit":
            break
        elif command == "Movej":
            joint1, joint2, joint3, joint4, joint5, joint6 = input("Enter joint angles: ").split()
            MoveJoint(command_sock, joint1, joint2, joint3, joint4, joint5, joint6)
        elif command == "Movel":
            x, y, z, rx, ry, rz = input("Enter TCP coordinates: ").split()
            MoveTCP(command_sock, x, y, z, rx, ry, rz)
        elif command == "tool":
            tool_state = input("Enter tool state (on/off): ")
            if tool_state == "on":
                Tool(command_sock, 24, 1, 0)
            elif tool_state == "off":
                Tool(command_sock, 24, 0, 1)
            else:
                print("Invalid tool state")
        elif command == "reqdata":
            #reqdata = input("Enter data request: ")
            ReqData(command_sock,data_sock)
        else:
            print("Invalid command")
    

    #MoveJoint(command_sock, 0, 10, 10, 0, 10, 10, 1, 1)

    connect_to_wifi("D315-5G", "airrobot315")