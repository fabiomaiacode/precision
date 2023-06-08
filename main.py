import sys
import sqlite3
import random
import string
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QColor, QCloseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, \
    QListWidgetItem, QStackedWidget, QLabel, QHBoxLayout, QPushButton, QTableWidgetItem, \
    QMenu, QLineEdit, QMessageBox, QDialog


from cadastrar import CadastrarWidget
from excluir import ExcluirWidget
from entrada import EntradaWidget
from saida import SaidaWidget
from relatorio import RelatorioWidget
from usuarios import UsuariosWidget

# Cria a tabela "products"
def create_products_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Cria a tabela "users"
def create_users_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            powers TEXT NOT NULL
        )
    """)

    # Verifica se o usuário "admin" já existe
    cursor.execute("SELECT id FROM users WHERE username = 'admin'")
    admin_exists = cursor.fetchone()

    # Verifica se o usuário "pmc" já existe
    cursor.execute("SELECT id FROM users WHERE username = 'pmc'")
    pmc_exists = cursor.fetchone()

    # Insere o usuário "admin" se não existir
    if not admin_exists:
        cursor.execute("""
            INSERT INTO users (username, password, powers)
            VALUES ('admin', 'admin', 'totais')
        """)

    # Insere o usuário "pmc" se não existir
    if not pmc_exists:
        cursor.execute("""
            INSERT INTO users (username, password, powers)
            VALUES ('pmc', 'pmc123', 'entrada, saída, relatório')
        """)

    conn.commit()
    conn.close()



class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(Qt.GlobalColor.white))
        self.setPalette(palette)
        self.setWindowTitle("Precision - Gestão de Estoque")
        self.setWindowIcon(QIcon("logo.png"))

        self.username_label = QLabel("Usuário:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Senha:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)
        self.setWindowTitle("Precision - Login")
        

    def show_centered(self):
        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry()
        window_rect = self.frameGeometry()
        x = screen_rect.center().x() - window_rect.width() // 2
        y = screen_rect.center().y() - window_rect.height() // 2
        self.move(x, y)
        self.show()

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.validate_login(username, password):
            self.accept()
        else:
            QMessageBox.warning(self, "Login Inválido", "Usuário ou senha incorretos!")

    def validate_login(self, username, password):
        # Aqui será feito a validação do usuário e senha com a base de dados no arquivo
        # database.db na tabela users
        # Neste exemplo, vamos considerar um usuário fixo para simplificar
        return username == "admin" and password == "admin"



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Precision - Gestão de Estoque")
        self.setWindowIcon(QIcon("logo.png"))

        self.left_menu_widget = QListWidget()

        self.left_menu_widget.currentRowChanged.connect(self.change_page)

        self.stacked_widget = QStackedWidget()

        layout = QHBoxLayout()
        layout.addWidget(self.left_menu_widget, 1)
        layout.addWidget(self.stacked_widget, 4)

        container = QWidget()
        container.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(container, 4)

        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        footer_label = QLabel("Secretaria de Serviços Públicos - Prefeitura de Caruaru - Precision Software")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addWidget(footer_label)
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(footer_widget)

        main_container = QWidget()
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

        self.create_logo()
        self.create_second_logo() 
        self.setup_menu()

        self.left_menu_widget.setStyleSheet("""
            QListWidget {
                background-color: #f0f0f0;
                border: none;
                padding: 0;
                margin: 0;
            }
            
            QListWidget::item {
                padding: 10px 8px;
                margin: 0;
                border: none;
            }
            
            QListWidget::item:hover {
                background-color: #0B5394;
                border: none;
            }
            
            QListWidget::item:selected {
                background-color: #888a89;
                color: #f5f5f5;
            }
            
            QListWidget::item:selected:active {
                background-color: #888a89;
                color: #f5f5f5;  /* Altere para a cor verde desejada */
            }
        """)

    def setup_menu(self):
            menu_items = [
                ("Cadastrar Produto", CadastrarWidget),
                ("Excluir Produto", ExcluirWidget),
                ("Entrada", EntradaWidget),
                ("Saída", SaidaWidget),
                ("Relatório", RelatorioWidget),
                ("Usuários", UsuariosWidget)
            ]

            font = self.left_menu_widget.font()
            font.setBold(True)
            self.left_menu_widget.setFont(font)

            self.left_menu_widget.setStyleSheet("""
                QListWidget::item:selected {
                    background-color: #000;
                    color: #888;
                }
                
                QListWidget::item:selected:active {
                    background-color: #000;
                    color: #888;
                }
            """)

            self.pages = {}  # Dicionário para armazenar as páginas por nome

            for i, (name, widget_class) in enumerate(menu_items):
                item = QListWidgetItem(name)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.left_menu_widget.addItem(item)

                widget = widget_class()
                self.pages[name] = widget  # Armazena a página no dicionário
                self.stacked_widget.addWidget(widget)

 
            self.left_menu_widget.setCurrentRow(0)  # Define o primeiro item do menu como selecionado por padrão
            self.change_page(0)  # Exibe a primeira página

    def change_page(self, current_row):
            # Obtem o item selecionado no menu
            item = self.left_menu_widget.item(current_row)
            if item is not None:
                # Obtem o nome do item selecionado
                name = item.text()

                # Obtem a página correspondente ao nome do item
                page = self.pages.get(name)
                if page is not None:
                    # Exibe a página correta no QStackedWidget
                    self.stacked_widget.setCurrentWidget(page)

    def create_logo(self):
        logo_item = QListWidgetItem(self.left_menu_widget)
        logo_pixmap = QPixmap("logo.png").scaled(QSize(150, 150))  # Redimensiona a imagem do logo
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_item.setSizeHint(logo_label.sizeHint())  # Ajusta o tamanho do item ao tamanho da imagem

        # Adiciona as propriedades ItemIsSelectable e ItemIsEnabled ao item da logo
        logo_item.setFlags(logo_item.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEnabled)

        self.left_menu_widget.addItem(logo_item)
        self.left_menu_widget.setItemWidget(logo_item, logo_label)

    def create_second_logo(self):
        second_logo_item = QListWidgetItem(self.left_menu_widget)
        second_logo_pixmap = QPixmap("logo2.png").scaled(QSize(150, 150))  # Redimensiona a imagem do segundo logo
        second_logo_label = QLabel()
        second_logo_label.setPixmap(second_logo_pixmap)
        second_logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        second_logo_item.setSizeHint(second_logo_label.sizeHint())  # Ajusta o tamanho do item ao tamanho da imagem

        # Adiciona as propriedades ItemIsSelectable e ItemIsEnabled ao item do segundo logo
        second_logo_item.setFlags(second_logo_item.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEnabled)

        self.left_menu_widget.addItem(second_logo_item)
        self.left_menu_widget.setItemWidget(second_logo_item, second_logo_label)
    

    def closeEvent(self, event: QCloseEvent):
        # Verifica se o usuário realmente deseja sair
        reply = QMessageBox.question(
            self,
            "Confirmação de Saída",
            "Deseja realmente sair?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )


        if reply == QMessageBox.StandardButton.Yes:
            # Se o usuário confirmar a saída, chame o método padrão de fechamento da janela
            event.accept()
        else:
            # Caso contrário, ignore o evento de fechamento
            event.ignore()

 
if __name__ == "__main__":
    create_products_table()  # Cria a tabela "products"
    create_users_table()  # Cria a tabela "users" e insere os usuários iniciais

    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        main_window = MainWindow()
        main_window.showMaximized()

        sys.exit(app.exec())