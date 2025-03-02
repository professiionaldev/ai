from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname", "Assistant")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

def TempDirectoryPath(Filename):
    return rf"{TempDirPath}\{Filename}"

def GraphicsDirectoryPath(Filename):
    return rf"{GraphicsDirPath}\{Filename}"

def SetMicrophoneStatus(Command):
    with open(TempDirectoryPath('Mic.data'), "w", encoding='utf-8') as file:
        file.write(Command)

def GetAssistantStatus():
    path = TempDirectoryPath('Status.data')
    if os.path.exists(path):
        with open(path, "r", encoding='utf-8') as file:
            return file.read()
    return ""

def ShowTextToScreen(Text):
    with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as file:
        file.write(Text)

class ChatSection(QWidget):
    
    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)

        self.setStyleSheet("background-color: black;")
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)

        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        movie.setScaledSize(QSize(480, 270))
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label, alignment=Qt.AlignRight)

        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px;")
        layout.addWidget(self.label, alignment=Qt.AlignRight)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.updateStatusText)
        self.timer.start(100)

    def loadMessages(self):
        global old_chat_message
        path = TempDirectoryPath('Responses.data')

        if os.path.exists(path):
            with open(path, "r", encoding='utf-8') as file:
                messages = file.read().strip()
                if messages and messages != old_chat_message:
                    self.addMessage(messages, "white")
                    old_chat_message = messages

    def updateStatusText(self):
        self.label.setText(GetAssistantStatus())

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        stacked_widget = QStackedWidget(self)
        chat_section = ChatSection()
        stacked_widget.addWidget(chat_section)

        self.setGeometry(0, 0, screen_width, screen_height)
        self.setStyleSheet("background-color: black;")

        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)

class CustomTopBar(QWidget):
    
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.initUI()
        self.stacked_widget = stacked_widget

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)

        home_button = QPushButton("  Home")
        home_button.setIcon(QIcon(GraphicsDirectoryPath("Home.png")))
        home_button.setStyleSheet("height:40px; background-color:white; color: black")
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        message_button = QPushButton("  Chat")
        message_button.setIcon(QIcon(GraphicsDirectoryPath("Chats.png")))
        message_button.setStyleSheet("height:40px; background-color:white; color: black")
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        minimize_button = QPushButton()
        minimize_button.setIcon(QIcon(GraphicsDirectoryPath("Minimize2.png")))
        minimize_button.setStyleSheet("background-color:white")
        minimize_button.clicked.connect(self.parent().showMinimized)

        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(GraphicsDirectoryPath('Maximize.png'))
        self.restore_icon = QIcon(GraphicsDirectoryPath('Minimize.png'))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setStyleSheet("background-color:white")
        self.maximize_button.clicked.connect(self.toggleMaximizeRestore)

        close_button = QPushButton()
        close_button.setIcon(QIcon(GraphicsDirectoryPath('Close.png')))
        close_button.setStyleSheet("background-color:white")
        close_button.clicked.connect(self.parent().close)

        title_label = QLabel(f" {Assistantname} AI  ")
        title_label.setStyleSheet("color: black; font-size: 18px; background-color:white")

        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)

    def toggleMaximizeRestore(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()
