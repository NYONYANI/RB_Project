import time
import robot_c

def text_control(robot,ROBOT_IP, COMMAND_PORT, DATA_PORT):
    robot = robot_c.Robot(ROBOT_IP, COMMAND_PORT, DATA_PORT)
    if (robot.connect()==0 ):
        robot.CobotInit()
        time.sleep(1)
        robot.pgmode_real()
        robot.MoveJoint(90, 30, -90, 60, -90, 0)
        robot.receive_data()
    else:
        print("Connection failed")
        exit()
    grab=[[143, -526, 108, 90, 0, -90],[143, -526, 14, 90, 0, -90]]
    print("Available commands: Movej, Movel, tool, reqdata, exit")
    while 1:
        robot.receive_data()
        command = input("Enter command: ")

        if command == "exit":
            return 0
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
            robot.sdw(speed)
        elif command == "show_state":
            robot.receive_data()
            robot.show_state()
            
        elif command == "shutdown":
            robot.shutdown()
        elif command == "reqdata":
            robot.receive_data()
        elif command == "grab":
            robot.Tool(24, 1, 0)
            time.sleep(1)
            print(grab[0][0],grab[0][1],grab[0][2],grab[0][3],grab[0][4],grab[0][5])
            robot.MoveTCP(143, -526, 108, 90, 0, -90)
            time.sleep(5)
            robot.MoveTCP(143, -526, 14, 90, 0, -90)
            #time.sleep(1)
            time.sleep(5)
            robot.Tool(24, 1, 0)
            
        else:
            print("Invalid command")