from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem
import sqlite3


class SaidaWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("REGISTRAR SAÍDA DE PRODUTO")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.search_label = QLabel("Procurar por Código ou Nome do Produto:")
        self.search_line_edit = QLineEdit()

        self.quantity_label = QLabel("Quantidade:")
        self.quantity_line_edit = QLineEdit()

        self.confirm_button = QPushButton("Confirmar Saída")
        self.confirm_button.clicked.connect(self.confirm_output)

        self.update_button = QPushButton("Atualizar")
        self.update_button.clicked.connect(self.load_product_list)

        layout.addWidget(title_label)
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_line_edit)
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_line_edit)
        layout.addWidget(self.confirm_button)
        layout.addWidget(self.update_button)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        self.load_product_list()


    def load_product_list(self):
        self.table_widget.clear()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT code, name, category, quantity FROM products")
        products = cursor.fetchall()

        self.table_widget.setRowCount(len(products))
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Código", "Nome", "Categoria", "Quantidade"])

        for row, product in enumerate(products):
            code_item = QTableWidgetItem(product[0])
            name_item = QTableWidgetItem(product[1])
            category_item = QTableWidgetItem(product[2])
            quantity_item = QTableWidgetItem(str(product[3]))

            self.table_widget.setItem(row, 0, code_item)
            self.table_widget.setItem(row, 1, name_item)
            self.table_widget.setItem(row, 2, category_item)
            self.table_widget.setItem(row, 3, quantity_item)

        self.table_widget.resizeColumnsToContents()
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        conn.close()

    def confirm_output(self):
        search_text = self.search_line_edit.text()
        quantity = self.quantity_line_edit.text()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            # Check if the search text is a code or name
            query = "UPDATE products SET quantity = quantity - ? WHERE code = ? OR name = ?"
            cursor.execute(query, (quantity, search_text, search_text))
            conn.commit()

            conn.close()

            self.search_line_edit.clear()
            self.quantity_line_edit.clear()

            print("Saída registrada com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao registrar saída: {e}")
