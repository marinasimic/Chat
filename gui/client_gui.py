from PySide6 import QtCore, QtWidgets
from backend.client import Client

client = Client()


class ConnectToServerWindow(QtWidgets.QWidget):
    def __init__(self, enterUsernameWindow):
        super().__init__()
        self.enterUsernameWindow = enterUsernameWindow

        self.setWindowTitle("Connect to server")

        self.button = QtWidgets.QPushButton("Done")
        self.button.setFixedWidth(50)
        self.errorLabel = QtWidgets.QLabel("")
        self.errorLabel.setStyleSheet("color: red")
        self.lineedit = QtWidgets.QLineEdit()
        self.lineedit.setFixedWidth(150)
        self.lineedit.setPlaceholderText("Enter chat server address")
        self.lineedit.returnPressed.connect(self.connect_to_server)
        self.lineedit.textChanged.connect(self.on_text_changed)

        self.layout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.Direction.TopToBottom, self)
        self.layout.addWidget(
            self.lineedit, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(
            self.errorLabel, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(
            self.button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.button.clicked.connect(self.connect_to_server)

    def on_text_changed(self, text):
        self.errorLabel.setText("")

    def show_enter_username_window(self):
        self.hide()
        self.enterUsernameWindow.show()

    @QtCore.Slot()
    def connect_to_server(self):
        server_address = str(self.lineedit.text())
        connection_result = client.connect_to_server(server_address)
        if not connection_result[0]:
            self.errorLabel.setText(connection_result[1])
        else:
            print(connection_result[1])
            self.show_enter_username_window()


class EnterUsernameWindow(QtWidgets.QWidget):
    def __init__(self, chatWindow):
        super().__init__()
        self.chatWindow = chatWindow

        self.setWindowTitle("Select your username")

        self.button = QtWidgets.QPushButton("Done")
        self.button.setFixedWidth(50)
        self.errorLabel = QtWidgets.QLabel("")
        self.errorLabel.setStyleSheet("color: red")

        self.lineedit = QtWidgets.QLineEdit()
        self.lineedit.setFixedWidth(150)
        self.lineedit.setPlaceholderText("Enter your username")
        self.lineedit.returnPressed.connect(self.connect)
        self.lineedit.textChanged.connect(self.on_text_changed)

        self.layout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.Direction.TopToBottom, self)
        self.layout.addWidget(
            self.lineedit, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(
            self.errorLabel, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(
            self.button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.button.clicked.connect(self.connect)

    def on_text_changed(self, text):
        self.errorLabel.setText("")

    def show_chat_window(self):
        self.hide()
        self.chatWindow.show()

    @QtCore.Slot()
    def connect(self):
        username = str(self.lineedit.text())
        result = client.enter_username(username)
        if not result[0]:
            self.errorLabel.setText(result[1])
            return

        self.show_chat_window()


class ChatWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Send")
        self.button.setFixedWidth(50)
        self.lineedit = QtWidgets.QLineEdit()
        self.lineedit.setFixedWidth(150)
        self.lineedit.setPlaceholderText("Enter your message")
        self.lineedit.returnPressed.connect(self.connect)

        self.chatBox = QtWidgets.QTextEdit()
        self.chatBox.setFixedSize(QtCore.QSize(150, 200))
        self.chatBox.setDisabled(True)

        self.layout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.Direction.TopToBottom, self)
        self.layout.addWidget(
            self.chatBox, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(
            self.lineedit, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(
            self.button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.button.clicked.connect(self.connect)

    def showEvent(self, event):
        self.setWindowTitle("Chatting at {0} as {1}".format(
            client.server_address, client.username))

    @QtCore.Slot()
    def connect(self):
        username = str(self.lineedit.text())
        result = client.enter_username(username)
        print(result[1])
        if not result[0]:
            return


def main():
    app = QtWidgets.QApplication([])

    chatWindow = ChatWindow()
    chatWindow.resize(400, 150)

    euWindow = EnterUsernameWindow(chatWindow)
    euWindow.resize(300, 150)

    ctsWindow = ConnectToServerWindow(euWindow)
    ctsWindow.resize(300, 150)
    ctsWindow.show()

    app.exec()
