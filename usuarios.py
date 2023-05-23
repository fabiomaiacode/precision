from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
import sqlite3


class UsuariosWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        title_label = QLabel("USUÁRIOS")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.username_label = QLabel("Usuário:")
        self.username_line_edit = QLineEdit()

        self.password_label = QLabel("Senha:")
        self.password_line_edit = QLineEdit()

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.setEnabled(False)

        layout.addWidget(title_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_line_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_line_edit)
        layout.addWidget(self.login_button)
        layout.addWidget(self.logout_button)


        # Adiciona espaço vertical para empurrar o conteúdo para baixo
        spacer_item = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer_item)

    def login(self):
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()

        # Implement your login logic here
        # This is just a placeholder
        print("Login successful!")

        self.username_line_edit.clear()
        self.password_line_edit.clear()

        self.login_button.setEnabled(False)
        self.logout_button.setEnabled(True)

    def logout(self):
        # Implement your logout logic here
        # This is just a placeholder
        print("Logout successful!")

        self.login_button.setEnabled(True)
        self.logout_button.setEnabled(False)
