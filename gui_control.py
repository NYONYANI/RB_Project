from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit,QTextEdit, QSlider,QLabel
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
import sys
import robot_c
from os import environ


font_path = "fonts/YourFont.ttf"
class MyWindow(QMainWindow):
    def __init__(self,ROBOT_IP, COMMAND_PORT, DATA_PORT, WIFI_SSID, parent=None):
        super().__init__()
        self.setWindowTitle("My Window")
        self.resize(400, 300)
        
        ui_file = "mainwindow.ui"
        loadUi(ui_file, self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.receive_data)
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




        self.ip_address = self.findChild(QLineEdit, 'IP_ADDRESS')
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

        
    
    def connect_to_ros(self):
        # Get the IP address from the text field
        ip = self.ip_address.text()
        self.robot.ip = ip
        if (self.robot.connect()==0 ):
            print("Connection successful")
            self.debug_msg.append("Connection successful")
            self.timer.start(500)
        else:
            print("Connection failed")
            self.debug_msg.append("Connection failed")
    def change_speed(self):
        speed = self.hs_base_speed.value() / 100.0
        self.robot.sdw(speed)
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
        if self.robot.robot_state.robot_state == 3:self.robot_state_Moving.setStyleSheet("background-color: green;")
        else:self.robot_state_Moving.setStyleSheet("background-color: white;")
        if self.robot.robot_state.robot_state == 1:self.robot_state_Idle.setStyleSheet("background-color: green;")
        else:self.robot_state_Idle.setStyleSheet("background-color: white;")

        if self.robot.robot_state.real_vs_simulation_mode == 0: self.mode_real.setStyleSheet("background-color: green;")
        else: self.mode_real.setStyleSheet("background-color: white;")

        if self.robot.robot_state.real_vs_simulation_mode == 1:self.mode_simulation.setStyleSheet("background-color: green;")
        else: self.mode_simulation.setStyleSheet("background-color: white;")

        if self.robot.robot_state.init_state_info == 1: self.LE_INIT_POWER.setStyleSheet("background-color: green;")
        if self.robot.robot_state.init_state_info == 2: self.LE_INIT_DEVICE.setStyleSheet("background-color: green;")
        if self.robot.robot_state.init_state_info == 3: self.LE_INIT_SYSTEM.setStyleSheet("background-color: green;")
        if self.robot.robot_state.init_state_info == 4: self.LE_INIT_ROBOT.setStyleSheet("background-color: green;")

        if self.robot.robot_state.tfb_digital_out[0] == 0:self.TOOL_OUT_ON.setStyleSheet("background-color: green;")
        else:self.TOOL_OUT_ON.setStyleSheet("background-color: white;")


def suppress_qt_warnings():
        environ["QT_DEVICE_PIXEL_RATIO"] = "0"
        environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        environ["QT_SCREEN_SCALE_FACTORS"] = "1"
        environ["QT_SCALE_FACTOR"] = "1"
if __name__ == "__main__":
    suppress_qt_warnings()
    import subprocess
    subprocess.call(["python", "main.py"])