import socket
import threading
from collections import deque

class IntermediateClient:
    def __init__(self, udp_group='233.0.0.1', udp_port=1502, tcp_port=1503):
        self.last_messages = deque(maxlen=5)
        self.current_message = ""
        
        # UDP
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_sock.bind(('', udp_port))
        mreq = socket.inet_aton(udp_group) + socket.inet_aton('0.0.0.0')
        self.udp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        # TCP
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_server.bind(('localhost', tcp_port))
        self.tcp_server.listen(5)
    
    def receive_udp(self):
        while True:
            data, _ = self.udp_sock.recvfrom(1024)
            message = data.decode('utf-8')
            if message != self.current_message:
                self.current_message = message
                self.last_messages.append(message)
                print(f"Новое сообщение: {message}")
    
    def handle_tcp(self, client_socket):
        messages = "\n".join(self.last_messages) if self.last_messages else "Нет сообщений"
        client_socket.send(messages.encode('utf-8'))
        client_socket.close()
    
    def start(self):
        print("Промежуточный клиент запущен")
        threading.Thread(target=self.receive_udp, daemon=True).start()
        
        while True:
            client_socket, addr = self.tcp_server.accept()
            print(f"Клиент подключен: {addr}")
            threading.Thread(target=self.handle_tcp, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    IntermediateClient().start()