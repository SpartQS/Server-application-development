import socket
import tkinter as tk
from tkinter import scrolledtext
import threading

class FinalClient:
    def __init__(self, host='localhost', port=1503):
        self.host = host
        self.port = port
        self.root = tk.Tk()
        self.root.title("Погода")
        self.root.geometry("500x300")
        
        # Кнопки
        self.connect_btn = tk.Button(self.root, text="Подключиться", command=self.connect)
        self.connect_btn.pack(pady=10)
        
        # Статус
        self.status = tk.Label(self.root, text="Не подключено", fg="red")
        self.status.pack()
        
        # Сообщения
        self.text_area = scrolledtext.ScrolledText(self.root, height=15)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.text_area.insert(tk.END, "Нажмите 'Подключиться'")
    
    def connect(self):
        def thread():
            try:
                self.status.config(text="Подключение...", fg="orange")
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((self.host, self.port))
                data = client_socket.recv(4096).decode('utf-8')
                client_socket.close()
                
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, data)
                self.status.config(text="Успешно подключено", fg="green")
            except:
                self.status.config(text="Ошибка подключения", fg="red")
        
        threading.Thread(target=thread, daemon=True).start()
    
    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    FinalClient().start()