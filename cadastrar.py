from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox
from PyQt6.QtCore import pyqtSignal
from datetime import date
import sqlite3
import random
import string


class CadastrarWidget(QWidget):
    product_registered = pyqtSignal()  # Sinal emitido quando um produto for cadastrado

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("CADASTRAR PRODUTO")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.code_label = QLabel("Código do Produto:")
        self.code_line_edit = QLineEdit()
        self.code_line_edit.setReadOnly(True)

        self.name_label = QLabel("Nome do Produto:")
        self.name_line_edit = QLineEdit()

        self.category_label = QLabel("Classificação do Produto:")
        self.category_combo_box = QComboBox()
        self.category_combo_box.addItems(["Higiene e Limpeza", "Expediente", "Copa e Cozinha", "Ferramentas", "Outros"])

        self.register_button = QPushButton("Cadastrar")
        self.register_button.clicked.connect(self.register_product)

        self.update_button = QPushButton("Atualizar")
        self.update_button.clicked.connect(self.update_product_list)

        layout.addWidget(title_label)
        layout.addWidget(self.code_label)
        layout.addWidget(self.code_line_edit)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_line_edit)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_combo_box)
        layout.addWidget(self.register_button)
        layout.addWidget(self.update_button)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        self.generate_product_code()
        self.load_product_list()

    def update_product_list(self):
        self.load_product_list()

    def generate_product_code(self):
        while True:
            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM products WHERE code = ?", (code,))
            count = cursor.fetchone()[0]

            conn.close()

            if count == 0:
                self.code_line_edit.setText(code)
                break

    def load_product_list(self):
        self.table_widget.clear()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT code, name, category, quantity FROM products")  # Inclui a coluna "quantity" na consulta SQL
        products = cursor.fetchall()

        self.table_widget.setRowCount(len(products))
        self.table_widget.setColumnCount(4)  # Atualiza para 4 colunas
        self.table_widget.setHorizontalHeaderLabels(["Código", "Nome", "Categoria", "Quantidade"])  # Inclui o rótulo da coluna "Quantidade"

        for row, product in enumerate(products):
            code_item = QTableWidgetItem(product[0])
            name_item = QTableWidgetItem(product[1])
            category_item = QTableWidgetItem(product[2])
            quantity_item = QTableWidgetItem(str(product[3]))  # Converte a quantidade para string e cria o item para a coluna "Quantidade"

            self.table_widget.setItem(row, 0, code_item)
            self.table_widget.setItem(row, 1, name_item)
            self.table_widget.setItem(row, 2, category_item)
            self.table_widget.setItem(row, 3, quantity_item)  # Define o item na coluna "Quantidade"

        self.table_widget.resizeColumnsToContents()
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        conn.close()


    def register_product(self):
        code = self.code_line_edit.text()
        name = self.name_line_edit.text()
        category = self.category_combo_box.currentText()

        if code and name:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            self.product_registered.emit()  # Emite o sinal após
            try:
                cursor.execute("INSERT INTO products (code, name, category) VALUES (?, ?, ?)", (code, name, category))
                conn.commit()
                conn.close()

                QMessageBox.information(self, "Cadastro de Produto", "Produto cadastrado com sucesso!")
                self.generate_product_code()
                self.name_line_edit.clear()
                self.load_product_list()
            except sqlite3.Error as e:
                print(f"Erro ao cadastrar produto: {e}")
        else:
            QMessageBox.warning(self, "Cadastro de Produto", "Por favor, preencha todos os campos.")

