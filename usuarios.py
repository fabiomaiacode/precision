from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,\
    QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QInputDialog

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
        self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)  # Define o modo de exibição do campo de senha

        self.powers_label = QLabel("Poderes:")
        self.powers_combo_box = QComboBox()
        self.powers_combo_box.addItems(["admin", "gestor", "comum"])

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(2)  # Número de colunas da tabela
        self.user_table.setHorizontalHeaderLabels(["Usuário", "Poderes"])
        self.user_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Impede a edição dos itens da tabela
        self.user_table.itemSelectionChanged.connect(self.update_delete_button_state)  # Conecta o sinal de seleção de itens

        self.insert_user_button = QPushButton("Inserir Usuário")
        self.insert_user_button.clicked.connect(self.insert_user)

        self.delete_user_button = QPushButton("Excluir Usuário")
        self.delete_user_button.clicked.connect(self.remove_user)
        self.delete_user_button.setEnabled(False)

        layout.addWidget(title_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_line_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_line_edit)
        layout.addWidget(self.powers_label)
        layout.addWidget(self.powers_combo_box)
        layout.addWidget(self.user_table)
        layout.addWidget(self.insert_user_button)
        layout.addWidget(self.delete_user_button)

        # Adiciona espaço vertical para empurrar o conteúdo para baixo
        spacer_item = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer_item)

        # Conexão com o banco de dados
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

        # Criação da tabela "users" se não existir
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT,
                password TEXT,
                powers TEXT
            )
        """)
        self.conn.commit()

        # Popula a tabela de usuários
        self.populate_user_table()

        # Atualiza o estado inicial do botão "Excluir Usuário"
        self.update_delete_button_state()

    def update_delete_button_state(self):
        # Habilita ou desabilita o botão "Excluir Usuário" com base na seleção de itens na tabela
        selected_items = self.user_table.selectedItems()
        self.delete_user_button.setEnabled(len(selected_items) > 0)

    def populate_user_table(self):
        # Limpa a tabela antes de popular
        self.user_table.clearContents()
        self.user_table.setRowCount(0)  # Define o número de linhas como zero

        # Busca todos os usuários do banco de dados
        self.cursor.execute("SELECT username, password, powers FROM users")
        users = self.cursor.fetchall()

        # Popula a tabela com os usuários
        self.user_table.setRowCount(len(users))
        for row, user in enumerate(users):
            username = user[0]
            password = user[1]
            powers = user[2]
            self.user_table.setItem(row, 0, QTableWidgetItem(username))
            self.user_table.setItem(row, 1, QTableWidgetItem(powers))


    def add_user(self, username, password, powers):
        # Insere o usuário no banco de dados
        self.cursor.execute("INSERT INTO users (username, password, powers) VALUES (?, ?, ?)", (username, password, powers))
        self.conn.commit()

        # Atualiza a tabela de usuários
        self.populate_user_table()

    def remove_user(self):
        # Lógica para excluir usuário da tabela
        selected_items = self.user_table.selectedItems()
        if selected_items:
            rows_to_delete = set()
            for item in selected_items:
                rows_to_delete.add(item.row())

            usernames = set()
            for row in rows_to_delete:
                username = self.user_table.item(row, 0).text()
                usernames.add(username)

            for username in usernames:
                # Exclui o usuário do banco de dados
                self.cursor.execute("DELETE FROM users WHERE username = ?", (username,))
                self.conn.commit()

            # Atualiza a tabela de usuários
            self.populate_user_table()

    def insert_user(self):
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()
        powers = self.powers_combo_box.currentText()

        if not username or not password:
            # Verifica se os campos estão preenchidos
            QMessageBox.warning(self, "Aviso", "Por favor, preencha todos os campos.")
            return

        # Solicita a entrada de duas senhas
        password_confirm, ok = QInputDialog.getText(self, "Confirmação de senha", "Digite a senha novamente:", QLineEdit.EchoMode.Password)
        if ok and password_confirm == password:
            # Insere o usuário no banco de dados
            self.add_user(username, password, powers)
            self.username_line_edit.clear()
            self.password_line_edit.clear()
        else:
            QMessageBox.warning(self, "Aviso", "As senhas não correspondem.")


