from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt6.QtCore import QThread, pyqtSignal
import asyncio
import websockets
import client

class WebSocketClient(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, uri):
        super().__init__()
        self.uri = uri

    async def connect_websocket(self):
        try:
            async with websockets.connect(self.uri) as websocket:
                self.websocket = websocket
                while True:
                    message = await websocket.recv()
                    self.message_received.emit(message)
        except websockets.ConnectionClosed:
            print("WebSocket connection closed")
        except Exception as e:
            print(f"Error: {e}")

    def run(self):
        asyncio.run(self.connect_websocket())

class ChatWindow(QWidget):
    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age
        self.init_ui()
        self.websocket_client = WebSocketClient("ws://82.181.21.121:8000/ws")
        self.websocket_client.message_received.connect(self.display_message)
        self.websocket_client.start()

    def init_ui(self):
        self.setWindowTitle("Chat Window")

        self.layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True) 
        self.layout.addWidget(self.chat_display)

        self.message_entry = QLineEdit()
        self.layout.addWidget(self.message_entry)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.setLayout(self.layout)

    def send_message(self):
        message = self.message_entry.text()
        if message:
            self.chat_display.append(f"{self.name}: {message}")
            self.message_entry.clear()
            asyncio.run(self.websocket_client.websocket.send(f"{self.name}: {message}"))

    def display_message(self, message):
        self.chat_display.append(message)

if __name__ == "__main__":
    app = QApplication([])
    info = client.Information()
    name, age = info.get_info()
    chat_window = ChatWindow(name, age)
    chat_window.show()
    app.exec()
