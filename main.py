from wifi import *
import robot_c
ROBOT_IP = '10.0.2.7'
COMMAND_PORT = 5000
DATA_PORT = 5001
WIFI_SSID = "RB5-850"


if __name__ == "__main__":
    connect_to_wifi(WIFI_SSID)
    robot = robot_c.Robot(ROBOT_IP, COMMAND_PORT, DATA_PORT)
    if (robot.connect()==0):
        robot.CobotInit()
        robot.pgmode_real()
    else:
        print("Connection failed")
        exit()
        

    #사용 가능한 명령어를 출력
    print("Available commands: Movej, Movel, tool, reqdata, exit")

    while robot.receive_data():
        command = input("Enter command: ")

        if command == "exit":
            break
        elif command == "Movej":
            joint1, joint2, joint3, joint4, joint5, joint6 = input("Enter joint angles: ").split()
            robot.MoveJoint(joint1, joint2, joint3, joint4, joint5, joint6)
        elif command == "Movel":
            x, y, z, rx, ry, rz = input("Enter TCP coordinates: ").split()
            robot.MoveTCP(x, y, z, rx, ry, rz)
            
        elif command == "tool":
            tool_state = input("Enter tool state (on/off): ")
            if tool_state == "on": robot.Tool( 24, 1, 0)
            elif tool_state == "off": robot.Tool(24, 0, 1)
            else: print("Invalid tool state")
        elif command == "set_speed":
            speed = input("Enter speed: ")
            robot.shw(speed)
        elif command == "show_state":
            robot.show_state()
        elif command == "shutdown":
            robot.shutdown()

        else:
            print("Invalid command")
        
    

    #MoveJoint(command_sock, 0, 10, 10, 0, 10, 10, 1, 1)

    #disconnect_to_wifi(reconnect_ssid)