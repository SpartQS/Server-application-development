import socket
import time

class UDPServer:
    def __init__(self, group='233.0.0.1', port=1502, filename='weather.txt'):
        self.group = group
        self.port = port
        self.filename = filename
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
    
    def read_message(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except:
            return "Сообщение по умолчанию"
    
    def start(self):
        print(f"Сервер запущен: {self.group}:{self.port}")
        last_message = ""
        while True:
            current_message = self.read_message()
            if current_message != last_message:
                self.sock.sendto(current_message.encode('utf-8'), (self.group, self.port))
                print(f"Отправлено: {current_message}")
                last_message = current_message
            time.sleep(10)

if __name__ == "__main__":
    UDPServer().start()