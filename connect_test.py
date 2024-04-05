import socket

# 클라이언트 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 IP 주소와 포트 설정
server_address = ('10.0.2.7', 5000)

# 서버 소켓에 연결 요청
a= client_socket.connect(server_address)

# 연결 확인 메시지 출력
print("서버 연결됨",a)

# 데이터 송수신
# ...

# 연결 종료
client_socket.close()
