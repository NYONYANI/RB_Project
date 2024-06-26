from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit,QTextEdit, QSlider,QLabel
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
import sys
import robot_c
from os import environ
import time

#import realsense

font_path = "fonts/YourFont.ttf"
class MyWindow(QMainWindow):
    def __init__(self,ROBOT_IP, COMMAND_PORT, DATA_PORT, WIFI_SSID, parent=None):
        super().__init__()
        self.setWindowTitle("My Window")
        self.resize(400, 300)
        

        ui_file = "mainwindow.ui"
        loadUi(ui_file, self)
        self.motion = []
        self.old_state = 0
        self.Possible_Move =True
        self.Motion_play = False
        self.motion_count = -1
        self.timer = QTimer()
        self.timer.timeout.connect(self.receive_data)
        self.start_flag = 1
        self.Start_time=0
        self.Next_Motion = False
        self.robot =  robot_c.Robot(ROBOT_IP, COMMAND_PORT, DATA_PORT)
        self.robot_state = robot_c.reqdata.RobotData()

        # Get the BTN_CONNECT_ROS button and IP_ADDRESS text field from the UI
        self.btn_connect_ros = self.findChild(QPushButton, 'BTN_CONNECT_ROS')
        self.btn_cobot_init = self.findChild(QPushButton, 'BTN_COBOT_INIT')
        self.btn_mode_real = self.findChild(QPushButton, 'BTN_MODE_REAL')
        self.btn_mode_simulation = self.findChild(QPushButton, 'BTN_MODE_SIMULATION')
        self.btn_speed_change = self.findChild(QPushButton, 'BTN_SPEED_CHANGE')
        self.btn_move_joint = self.findChild(QPushButton, 'BTN_SEND_JOINT_POS')
        self.btn_move_tcp = self.findChild(QPushButton, 'BTN_SEND_TCP_POS')
        self.tool_on = self.findChild(QPushButton, 'BTN_TOOL_ON')
        self.tool_off = self.findChild(QPushButton, 'BTN_TOOL_OFF')
        self.clear_debug = self.findChild(QPushButton, 'BTN_CLEAR_LINE')
        self.robot_pos_reset = self.findChild(QPushButton, 'BTN_ROBOT_POS_RES')
        self.btn_motion_save = self.findChild(QPushButton, 'BTN_MOTION_SAVE')
        self.btn_motion_play = self.findChild(QPushButton, 'BTN_MOTION_PLAY')
        self.btn_motion_clear = self.findChild(QPushButton, 'BTN_MOTION_CLEAR')
        self.btn_motion_delay = self.findChild(QPushButton, 'BTN_MOTION_DELAY')
        #QAction으로 만들어진 save_Action 버튼 기능 추가
        self.actionSAVE.triggered.connect(self.save_action)
        self.actionLOAD.triggered.connect(self.load_action)

        self.ip_address = self.findChild(QLineEdit, 'IP_ADDRESS')
        self.delay_time = self.findChild(QLineEdit, 'LE_DELAY')
        self.debug_msg = self.findChild(QTextEdit, 'DEBUG_MSG')

        self.hs_base_speed = self.findChild(QSlider, 'HS_BASE_SPEED')
        self.lb_base_speed = self.findChild(QLabel, 'LB_BASE_SPEED')



        self.btn_connect_ros.clicked.connect(self.connect_to_ros)
        self.hs_base_speed.setRange(0, 100)

        self.btn_cobot_init.clicked.connect(self.cobot_init)
        self.btn_mode_real.clicked.connect(self.set_mode_real)
        self.btn_mode_simulation.clicked.connect(self.set_mode_simulation)
        self.hs_base_speed.valueChanged.connect(self.update_label)
        self.btn_move_joint.clicked.connect(self.move_joint)
        self.btn_move_tcp.clicked.connect(self.move_tcp)
        self.btn_speed_change.clicked.connect(self.change_speed)
        self.tool_on.clicked.connect(self.set_tool_on)
        self.tool_off.clicked.connect(self.set_tool_off)
        self.clear_debug.clicked.connect(self.debug_msg.clear)
        self.robot_pos_reset.clicked.connect(self.set_robot_pos_reset)
        self.btn_motion_save.clicked.connect(self.motion_save)
        self.btn_motion_play.clicked.connect(self.motion_play)
        self.btn_motion_clear.clicked.connect(self.motion.clear)
        self.btn_motion_delay.clicked.connect(self.motion_delay)
      
    def print_hello_world(self):
        print('Hello World')


    def connect_to_ros(self):
        # Get the IP address from the text field
        ip = self.ip_address.text()
        self.robot.ip = ip
        if (self.robot.connect()==0 ):
            print("Connection successful")
            self.debug_msg.append("Connection successful")
            self.timer.start(10)
        else:
            print("Connection failed")
            self.debug_msg.append("Connection failed")
    def change_speed(self):
        speed = self.hs_base_speed.value() / 100.0
        self.robot.sdw(speed)
    def save_action(self):
        file = open("action.txt", 'w')
        for i in range(len(self.motion)):
            if self.motion[i][0] == 'M':
                file.write("M")
                for j in range(6):
                    file.write(" "+str(self.motion[i][1][j]))
                for j in range(2):
                    file.write(" "+str(self.motion[i][2][j]))
                file.write("\n")
            elif self.motion[i][0] == 'D':
                file.write("D "+str(self.motion[i][1])+"\n")
        file.close()
        self.debug_msg.append("Action saved")

    def load_action(self):
        file = open("action.txt", 'r')
        self.motion.clear()
        while True:
            line = file.readline()
            if not line: break
            line = line.split()
            if line[0] == 'M':
                self.motion.append(['M',[float(line[1]),float(line[2]),float(line[3]),float(line[4]),float(line[5]),float(line[6])],[float(line[7]),float(line[8])]])
            elif line[0] == 'D':
                self.motion.append(['D',int(line[1])])
        file.close()
        self.debug_msg.append("Action loaded")
    def update_label(self, value):
        self.lb_base_speed.setText(str(value)+"%")

    def cobot_init(self):
        self.robot.CobotInit()
        self.debug_msg.append("Cobot Init")
    def set_mode_real(self):
        self.robot.pgmode_real()
    def set_mode_simulation(self):
        self.robot.pgmode_simulation()
    def set_robot_pos_reset(self):
        self.robot.MoveJoint(90, 30, -90, 60, -90, 0)
    def move_joint(self):
        joint1 = self.SET_JNT_POS_J1.text()
        joint2 = self.SET_JNT_POS_J2.text()
        joint3 = self.SET_JNT_POS_J3.text()
        joint4 = self.SET_JNT_POS_J4.text()
        joint5 = self.SET_JNT_POS_J5.text()
        joint6 = self.SET_JNT_POS_J6.text()

        self.robot.MoveJoint(joint1, joint2, joint3, joint4, joint5, joint6)
        self.debug_msg.append("Moving joints to: "+joint1+", "+joint2+", "+joint3+", "+joint4+", "+joint5+", "+joint6)
    def set_tool_on(self):
        self.debug_msg.append(str(self.robot.robot_state.tfb_digital_out))
        self.robot.Tool(24,0, 1)
        self.debug_msg.append("Tool on")
    def set_tool_off(self):
        self.debug_msg.append(str(self.robot.robot_state.tfb_digital_out))
        self.robot.Tool(24, 1, 0)
        self.debug_msg.append("Tool off")
    def move_tcp(self):
        x = self.SET_TCP_POS_X.text()
        y = self.SET_TCP_POS_Y.text()
        z = self.SET_TCP_POS_Z.text()
        rx = self.SET_TCP_POS_RX.text()
        ry = self.SET_TCP_POS_RY.text()
        rz = self.SET_TCP_POS_RZ.text()

        self.robot.MoveTCP(x, y, z, rx, ry, rz)
        self.debug_msg.append("Moving TCP to: "+x+", "+y+", "+z+", "+rx+", "+ry+", "+rz)
    def motion_save(self):
        self.motion.append(['M',self.robot.robot_state.jnt_ang,self.robot.robot_state.tfb_digital_out])
        self.debug_msg.append("Motion saved")
    def motion_play(self):
        self.debug_msg.append("Playing motion")
        self.debug_msg.append(str(len(self.motion)))
        self.Motion_play = True
        self.motion_count = 0
        self.Start_time = 0
        self.start_flag = False
        self.Next_Motion = False
        
        
            
    def motion_clear(self):
        self.motion.clear()
        self.debug_msg.append("Motion cleared")
    
    def motion_delay(self):
        delay = self.delay_time.text()
        self.debug_msg.append("Delay: "+delay)
        #time.sleep(int(delay))
        self.motion.append(['D',int(delay)])
    def receive_data(self):
        self.robot.receive_data()
        self.JNT_REF_1.setText(str(self.robot.robot_state.jnt_ref[0]))
        self.JNT_REF_2.setText(str(self.robot.robot_state.jnt_ref[1]))
        self.JNT_REF_3.setText(str(self.robot.robot_state.jnt_ref[2]))
        self.JNT_REF_4.setText(str(self.robot.robot_state.jnt_ref[3]))
        self.JNT_REF_5.setText(str(self.robot.robot_state.jnt_ref[4]))
        self.JNT_REF_6.setText(str(self.robot.robot_state.jnt_ref[5]))
        self.JNT_ENC_1.setText(str(self.robot.robot_state.jnt_ang[0]))
        self.JNT_ENC_2.setText(str(self.robot.robot_state.jnt_ang[1]))
        self.JNT_ENC_3.setText(str(self.robot.robot_state.jnt_ang[2]))
        self.JNT_ENC_4.setText(str(self.robot.robot_state.jnt_ang[3]))
        self.JNT_ENC_5.setText(str(self.robot.robot_state.jnt_ang[4]))
        self.JNT_ENC_6.setText(str(self.robot.robot_state.jnt_ang[5]))
        self.TCP_REF_X.setText(str(self.robot.robot_state.tcp_ref[0]))
        self.TCP_REF_Y.setText(str(self.robot.robot_state.tcp_ref[1]))
        self.TCP_REF_Z.setText(str(self.robot.robot_state.tcp_ref[2]))
        self.TCP_REF_RX.setText(str(self.robot.robot_state.tcp_ref[3]))
        self.TCP_REF_RY.setText(str(self.robot.robot_state.tcp_ref[4]))
        self.TCP_REF_RZ.setText(str(self.robot.robot_state.tcp_ref[5]))
        if self.robot.robot_state.robot_state == 3:
            self.robot_state_Moving.setStyleSheet("border-radius: 10px;background-color: green;")
        else:
            self.robot_state_Moving.setStyleSheet("border-radius: 10px;background-color:rgb(244, 248, 247);")
        if self.robot.robot_state.robot_state == 1:
            self.robot_state_Idle.setStyleSheet("border-radius: 10px;background-color: green;")
        else:self.robot_state_Idle.setStyleSheet("border-radius: 10px;background-color: rgb(244, 248, 247);")
#####################모션 실행할 코드 부분#############################
        
            #위에 if문을 효율적으로 바꿔줘
        
        if self.robot.robot_state.robot_state == 1 and self.robot.robot_state.robot_state != self.old_state:
            #self.debug_msg.append("로봇이 대기중입니다.")
            self.Can_Motion_play = True
        elif self.robot.robot_state.robot_state == 3:
            #self.debug_msg.append("로봇이 움직이고 있습니다.")
            self.Can_Motion_play = False
        

        if self.Motion_play and(self.Can_Motion_play or self.Start_time != 0 or self.Next_Motion):
            #self.debug_msg.append("Motion_play:%d,C_M_P:%d S_t:%d N_M:%d"%(self.Motion_play,self.Can_Motion_play,self.Start_time,self.Next_Motion))
            if self.motion[self.motion_count][0] == 'M':
                    self.Next_Motion = False
                    self.debug_msg.append("모션을 실행합니다.Motion play:%d"%self.motion_count)
                    MJ = self.motion[self.motion_count]
                    self.robot.MoveJoint(MJ[1][0],MJ[1][1],MJ[1][2],MJ[1][3],MJ[1][4],MJ[1][5])
                    self.robot.Tool(24,MJ[2][0],MJ[2][1])
                    self.motion_count += 1
                    time.sleep(0.1)

            elif self.motion[self.motion_count][0] == 'D':
                if self.Start_time == 0:
                    self.debug_msg.append("딜레이를 시작합니다. %d: %d 초"%(self.motion_count,int(self.motion[self.motion_count][1])))
                    self.Start_time = time.time()
                if (time.time() - self.Start_time) > self.motion[self.motion_count][1]:
                    self.debug_msg.append("딜레이가 끝났습니다.")
                    self.motion_count += 1
                    self.Start_time = 0
                    self.Next_Motion = True

            if len(self.motion) == self.motion_count:
                self.Motion_play = False
                self.debug_msg.append("모션 재생이 끝났습니다.")

#####################실행할 코드 부분 끝#############################           
        self.old_state = self.robot.robot_state.robot_state
        if self.robot.robot_state.real_vs_simulation_mode == 0: 
            self.mode_real.setStyleSheet("border-radius: 10px;\nbackground-color: green;")
        else: self.mode_real.setStyleSheet("border-radius: 10px;\nbackground-color: rgb(244, 248, 247);")

        if self.robot.robot_state.real_vs_simulation_mode == 1:self.mode_simulation.setStyleSheet("background-color: green;")
        else: self.mode_simulation.setStyleSheet("background-color: white;")

        if self.robot.robot_state.init_state_info == 1: self.LE_INIT_POWER.setStyleSheet("border-radius: 10px;\nbackground-color: green;")
        if self.robot.robot_state.init_state_info == 2: self.LE_INIT_DEVICE.setStyleSheet("border-radius: 10px;\nbackground-color: green;")
        if self.robot.robot_state.init_state_info == 3: self.LE_INIT_SYSTEM.setStyleSheet("border-radius: 10px;\nbackground-color: green;")
        if self.robot.robot_state.init_state_info == 4: self.LE_INIT_ROBOT.setStyleSheet("border-radius: 10px;\nbackground-color: green;")
        if self.robot.robot_state.init_state_info == 6: 
            self.LE_INIT_POWER.setStyleSheet("border-radius: 10px;\nbackground-color: green;")
            self.LE_INIT_DEVICE.setStyleSheet("border-radius: 10px;\nbackground-color: green;")
            self.LE_INIT_SYSTEM.setStyleSheet("border-radius: 10px;\nbackground-color: green;")
            self.LE_INIT_ROBOT.setStyleSheet("border-radius: 10px;\nbackground-color: green;")


        if self.robot.robot_state.tfb_digital_out[0] == 0:
            self.TOOL_OUT_ON.setStyleSheet("border-radius: 10px;\nbackground-color: rgb(244, 248, 247);\nbackground-color: green;")
            self.TOOL_OUT_OFF.setStyleSheet("border-radius: 10px;\nbackground-color: rgb(244, 248, 247);\nbackground-color: rgb(244, 248, 247);")
        else:
            self.TOOL_OUT_ON.setStyleSheet("border-radius: 10px;\nbackground-color: rgb(244, 248, 247);\nbackground-color: white;")
            self.TOOL_OUT_OFF.setStyleSheet("border-radius: 10px;\nbackground-color: rgb(244, 248, 247);\nbackground-color: rgb(244, 248, 247);")
        

def suppress_qt_warnings():
        environ["QT_DEVICE_PIXEL_RATIO"] = "0"
        environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        environ["QT_SCREEN_SCALE_FACTORS"] = "1"
        environ["QT_SCALE_FACTOR"] = "1"
if __name__ == "__main__":
    suppress_qt_warnings()
    import subprocess
    subprocess.call(["python", "main.py"])