import sys
import cohere
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class AIThread(QThread):
    update_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, api_key, message):
        QThread.__init__(self)
        self.api_key = api_key
        self.message = message

    def run(self):
        try:
            co = cohere.Client(api_key=self.api_key)
            stream = co.chat_stream(
                model='c4ai-aya-23',
                message=self.message,
                temperature=0.3,
                chat_history=[],
                prompt_truncation='AUTO',
                connectors=[]
            )
            for event in stream:
                if event.event_type == "text-generation":
                    self.update_signal.emit(event.text)
        except Exception as e:
            self.error_signal.emit(str(e))

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.chat_history = []
        self.api_key = "YRWmAS2MWCdFYP5J3sEP4W7gu8mCIhc2qczkSC8N"  # API anahtarınızı buraya girin

    def initUI(self):
        self.setWindowTitle('Gelişmiş AI Sohbet Arayüzü')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('chat_icon.png'))  # Simge ekleyin (dosya yolunu değiştirin)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setFont(QFont('Arial', 12))
        layout.addWidget(self.chat_area)

        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setFont(QFont('Arial', 12))
        self.input_box.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_box)

        send_button = QPushButton('Gönder')
        send_button.clicked.connect(self.send_message)
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        input_layout.addWidget(send_button)

        layout.addLayout(input_layout)

    def send_message(self):
        user_message = self.input_box.text().strip()
        if not user_message:
            return

        self.chat_area.append(f"<b>Siz:</b> {user_message}")
        self.input_box.clear()
        self.chat_history.append(f"Kullanıcı: {user_message}")

        self.chat_area.append("<b>AI:</b> ")
        self.ai_thread = AIThread(self.api_key, user_message)
        self.ai_thread.update_signal.connect(self.update_chat)
        self.ai_thread.error_signal.connect(self.show_error)
        self.ai_thread.start()

    def update_chat(self, text):
        self.chat_area.insertPlainText(text)
        self.chat_area.ensureCursorVisible()
        QApplication.processEvents()

    def show_error(self, error_message):
        QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {error_message}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())