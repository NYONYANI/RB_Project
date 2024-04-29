from wifi import *
import time
import text_control # type: ignore
import gui_control # type: ignore
import sys
from PyQt5.QtWidgets import QApplication

ROBOT_IP = '10.0.2.7'
COMMAND_PORT = 5000
DATA_PORT = 5001
WIFI_SSID = "RB5-850"

TEXT_CONTROL = False
GUI_CONTROL=True


if __name__ == "__main__":
      
    if TEXT_CONTROL:
        text_control(ROBOT_IP, COMMAND_PORT, DATA_PORT)
    elif GUI_CONTROL:
        app = QApplication(sys.argv)
        gui = gui_control.MyWindow(ROBOT_IP, COMMAND_PORT, DATA_PORT, WIFI_SSID)
        gui.show()
        sys.exit(app.exec())
      
    
        
        
    