import socket
import reqdata

class Robot:
    def __init__(self, ip, command_port, data_port):
        self.command_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.command_port = command_port
        self.data_port = data_port
        self.robot_state = reqdata.RobotData()
        print("success")

    def connect(self):
        try:
            self.command_sock.connect((self.ip, self.command_port))
            self.data_sock.connect((self.ip, self.data_port))
            print('Connected to robot')
        except Exception as e:
            print(f'Error connecting to robot: {e}')
            return -1
        return 0
    def send_command(self, command):
        try:
            #print(command.encode())
            self.command_sock.sendall(command.encode())
        except Exception as e:
            print(f'Error sending command: {e}')

    def receive_data(self):
        try:
            self.data_sock.sendall("reqdata".encode())
            receive_data = self.data_sock.recv(1024)  # The total size of the structure
            #print(self.receive_data)
            self.robot_state.unpack(receive_data)
            
            return 1
        except Exception as e:
            print(f'Error receiving data: {e}')
        return 0

    def check_connection(self):
        try:
            self.command_sock.getpeername()
            print('Connection successful')
        except Exception as e:
            print(f'Connection failed: {e}')

    def CobotInit(self):
        self.send_command("mc jall init")

    def MoveJoint(self, joint1, joint2, joint3, joint4, joint5, joint6, spd = -1, acc = -1):
        while 1:
            self.receive_data()
            if self.robot_state.robot_state ==1:break
            
        self.send_command(f"jointall {spd}, {acc}, {joint1}, {joint2}, {joint3}, {joint4}, {joint5}, {joint6}")

    def MoveTCP(self, x, y, z, rx, ry, rz, spd = -1, acc = -1):
        while 1:
            self.receive_data()
            if self.robot_state.robot_state ==1: break

        self.send_command(f"movetcp {spd}, {acc}, {x}, {y}, {z}, {rx}, {ry}, {rz}")
    #tool 작동 코드 전압, d0, d1 로 구성
    def Tool(self, voltage, d0, d1):
        self.send_command(f"tool_out {voltage}, {d0}, {d1}")

    def pgmode_real(self):
        self.send_command(f"pgmode real")
    def pgmode_simulation(self):
        self.send_command(f"pgmode simulation")    
    def  shutdown(self):
        self.send_command(f"shutdown")
    def sdw(self,speed):
        self.send_command(f"sdw default_speed {speed}") 
    def show_state(self):
        print("joint_ref: ", self.robot_state.jnt_ref)
        print("joint_ang: ", self.robot_state.jnt_ang)
        print("tcp_ref: ", self.robot_state.tcp_ref)
        print("tcp_pos: ", self.robot_state.tcp_pos)
        print("robot_default_speed: ", self.robot_state.default_speed)
