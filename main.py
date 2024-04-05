from wifi import connect_to_wifi
from robot import send_command, receive_data, check_connection, CobotInit, MoveJoint, MoveTCP

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

    MoveJoint(command_sock, 0, 10, 10, 0, 10, 10, 1, 1)

    connect_to_wifi("D315-5G", "airrobot315")