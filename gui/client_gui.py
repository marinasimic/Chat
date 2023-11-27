from PySide6 import QtCore, QtWidgets, QtGui
from backend.client import Client

client = Client()


class ConnectToServerWindow(QtWidgets.QWidget):
    def __init__(self, enterUsernameWindow):
        super().__init__()
        self.enterUsernameWindow = enterUsernameWindow

        self.setWindowTitle("Connect to server")

        self.button = QtWidgets.QPushButton("Done")
        self.button.setFixedWidth(50)
        self.button.clicked.connect(self.connect_to_server)

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
            self.show_enter_username_window()


class EnterUsernameWindow(QtWidgets.QWidget):
    def __init__(self, chatWindow):
        super().__init__()
        self.chatWindow = chatWindow

        self.setWindowTitle("Select your username")

        self.button = QtWidgets.QPushButton("Done")
        self.button.setFixedWidth(50)
        self.button.clicked.connect(self.connect)

        self.errorLabel = QtWidgets.QLabel("")
        self.errorLabel.setStyleSheet("color: red")

        self.lineedit = QtWidgets.QLineEdit()
        self.lineedit.setFixedWidth(150)
        self.lineedit.setPlaceholderText("Enter your username")
        self.lineedit.returnPressed.connect(self.connect)
        self.lineedit.textChanged.connect(self.on_text_changed)
        pattern = QtCore.QRegularExpression('[^<]*')
        validator = QtGui.QRegularExpressionValidator(pattern, self.lineedit)
        self.lineedit.setValidator(validator)

        self.layout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.Direction.TopToBottom, self)
        self.layout.addWidget(
            self.lineedit, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(
            self.errorLabel, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(
            self.button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

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
        self.button.clicked.connect(self.send_message)

        self.lineedit = QtWidgets.QLineEdit()
        self.lineedit.setFixedWidth(150)
        self.lineedit.setPlaceholderText("Enter your message")
        self.lineedit.returnPressed.connect(self.send_message)
        self.lineedit.setFocus()

        self.chatBox = QtWidgets.QTextEdit()
        self.chatBox.setFixedSize(QtCore.QSize(150, 200))
        self.chatBox.setReadOnly(True)
        self.chatBox.ensureCursorVisible()

        self.activeUsers = QtWidgets.QTextEdit()
        self.activeUsers.setFixedSize(QtCore.QSize(70, 200))
        self.activeUsers.setReadOnly(True)

        self.chatTimer = QtCore.QTimer(self)
        self.chatTimer.timeout.connect(self.update_chat)
        self.usersTimer = QtCore.QTimer(self)
        self.usersTimer.timeout.connect(self.update_active_users)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(
            self.chatBox, 0, 0, 1, 1)
        self.layout.addWidget(
            self.activeUsers, 0, 1, 1, 1)
        self.layout.addWidget(
            self.lineedit, 1, 0, 1, 2)
        self.layout.addWidget(
            self.button, 2, 0, 1, 2)

    def showEvent(self, event):
        self.setWindowTitle("Chatting at {0} as {1}".format(
            client.server_address, client.username))

        self.chatTimer.start(500)
        self.usersTimer.start(2000)

    def closeEvent(self, event):
        event.ignore()
        client.stop_receiving_messages()
        self.close()

    def update_chat(self):
        messages = client.get_messages()
        for message in messages:
            if len(message) == 2:
                self.chatBox.insertHtml("<b>" + message[0] + "</b>: ")
                self.chatBox.insertPlainText(message[1])
                self.chatBox.insertHtml("<br>")
            else:
                self.chatBox.insertHtml("<span style=\"color:red;\">{}<span><br>".format(message[0]))
            self.chatBox.verticalScrollBar().setValue(self.chatBox.verticalScrollBar().maximum())

    def update_active_users(self):
        active_users = client.get_active_users()
        self.activeUsers.setHtml(active_users)

    @QtCore.Slot()
    def send_message(self):
        message = str(self.lineedit.text())
        client.send_message(message)
        self.lineedit.setText("")


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
