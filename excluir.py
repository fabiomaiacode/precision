from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, \
    QMenu, QMessageBox, QTableWidget, QApplication, QTableWidgetItem
from PyQt6.QtCore import pyqtSignal
import sqlite3


class ExcluirWidget(QWidget):
    product_deleted = pyqtSignal()  # Sinal emitido quando um produto for excluído

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("EXCLUIR PRODUTO")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.search_label = QLabel("Procurar por Código, Nome do Produto ou clique com o botão direito do mouse sobre o produto que deseja excluir :")
        self.search_line_edit = QLineEdit()

        self.delete_button = QPushButton("Excluir")
        self.delete_button.clicked.connect(self.delete_product)

        self.update_button = QPushButton("Atualizar")
        self.update_button.clicked.connect(self.load_product_list)

        layout.addWidget(title_label)
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_line_edit)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.update_button)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        self.load_product_list()

        # Conecta o sinal de menu de contexto à ação de exclusão
        self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_context_menu)

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



    def delete_product(self):
        search_text = self.search_line_edit.text()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            # Check if the search text is a code or name
            query = "DELETE FROM products WHERE code = ? OR name = ?"
            cursor.execute(query, (search_text, search_text))
            affected_rows = cursor.rowcount  # Número de linhas afetadas

            conn.commit()
            conn.close()

            if affected_rows > 0:
                self.search_line_edit.clear()
                self.load_product_list()
                self.product_deleted.emit()  # Emitir o sinal após excluir o produto

                # Exibe mensagem de sucesso
                QMessageBox.information(self, "Sucesso", "Produto excluído com sucesso!")
                QApplication.processEvents()  # Processa eventos pendentes

                print("Produto excluído com sucesso!")
            else:
                # Nenhum produto encontrado para exclusão
                QMessageBox.information(self, "Erro ao excluir produto!", "Produto não encontrado. Tente novamente.")
                QApplication.processEvents()  # Processa eventos pendentes
        except sqlite3.Error as e:
            QMessageBox.information(self, "Erro ao excluir produto!", f"Erro ao excluir produto: {e}")
            QApplication.processEvents()  # Processa eventos pendentes

    def show_context_menu(self, position):
        # Verifica se uma linha da tabela foi selecionada
        if self.table_widget.selectedItems():
            menu = QMenu(self)

            # Ação de exclusão
            delete_action = QAction("Excluir", self)
            delete_action.triggered.connect(self.delete_selected_product)  # Correção aqui
            menu.addAction(delete_action)

            # Exibe o menu de contexto na posição do cursor
            menu.exec(self.table_widget.viewport().mapToGlobal(position))

    def delete_selected_product(self):
        selected_rows = set()
        for item in self.table_widget.selectedItems():
            selected_rows.add(item.row())

        if selected_rows:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            try:
                for row in selected_rows:
                    code_item = self.table_widget.item(row, 0)  # Obtem o item da coluna 0 (código)
                    code = code_item.text()

                    # Exclui o produto pelo código
                    query = "DELETE FROM products WHERE code = ?"
                    cursor.execute(query, (code,))
                    affected_rows = cursor.rowcount

                    if affected_rows > 0:
                        self.load_product_list()

                conn.commit()
                conn.close()

                # Exibir mensagem de sucesso
                QMessageBox.information(self, "Sucesso", "Produto(s) excluído(s) com sucesso!")
                QApplication.processEvents()  # Processa eventos pendentes

                print("Produto(s) excluído(s) com sucesso!")
            except sqlite3.Error as e:
                QMessageBox.information(self, "Erro ao excluir produto!", f"Erro ao excluir produto: {e}")
                QApplication.processEvents()  # Processa eventos pendentes



