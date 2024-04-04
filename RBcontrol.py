import socket

# IP address and ports
ip_address = '10.0.2.7'
send_port = 5000
receive_port = 5001

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the robot arm
    client_socket.connect((ip_address, send_port))
    print("Connected to the robot arm!")

    # Send data to the robot arm
    # ...

except ConnectionRefusedError:
    print("Failed to connect to the robot arm.")

finally:
    # Close the socket
    client_socket.close()