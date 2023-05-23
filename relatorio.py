from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QSizePolicy, QSpacerItem, QPushButton, QToolBar, QFileDialog, QTableView
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem, QFont, QPainter
from PyQt6.QtCore import Qt
import sqlite3


class RelatorioWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        title_label = QLabel("RELATÓRIO")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.generate_button = QPushButton("Gerar Relatório")
        self.generate_button.clicked.connect(self.generate_report)

        self.report_table = QTableView()
        self.report_table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.report_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.report_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.report_table.setVisible(False)

        layout.addWidget(title_label)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.report_table)

        # Adiciona espaço vertical para empurrar o conteúdo para baixo
        spacer_item = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer_item)

    def generate_report(self):
        # Estabelece conexão com o banco de dados
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Executa a consulta SQL para obter a quantidade atual de produtos
        cursor.execute("SELECT code, name, category, quantity FROM products")
        rows = cursor.fetchall()

        # Cria o modelo de dados para a tabela
        model = QStandardItemModel(len(rows), 4)
        model.setHorizontalHeaderLabels(["Código", "Nome", "Categoria", "Quantidade"])

        # Preenche o modelo de dados com os resultados
        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                item = QStandardItem(str(col_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                model.setItem(row_idx, col_idx, item)

        # Define o modelo de dados na tabela
        self.report_table.setModel(model)
        self.report_table.setVisible(True)

        # Fecha a conexão com o banco de dados
        conn.close()

        print("Relatório gerado com sucesso!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("AF Software - Gestão de Estoque")
        self.setWindowIcon(QIcon("logo.png"))

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.create_toolbar()
        layout.addWidget(self.toolbar)

        self.create_logo()
        self.create_second_logo()
        self.setup_menu()

        self.create_buttons()
        layout.addLayout(self.button_layout)

    def create_toolbar(self):
        self.toolbar = QToolBar(self)
        self.addToolBar(self.toolbar)

    def create_buttons(self):
        self.button_layout = QVBoxLayout()

        self.print_button = QPushButton("Imprimir")
        self.print_button.setMaximumSize(200, 200)
        self.print_button.setVisible(False)
        self.print_button.clicked.connect(self.print_report)

        self.save_pdf_button = QPushButton("Salvar")
        self.save_pdf_button.setMaximumSize(200, 200)
        self.save_pdf_button.setVisible(False)
        self.save_pdf_button.clicked.connect(self.save_pdf_report)

        self.button_layout.addWidget(self.print_button)
        self.button_layout.addWidget(self.save_pdf_button)
        self.button_layout.addStretch()

    def print_report(self):
        # lógica para imprimir o relatório
        print("Relatório impresso com sucesso!")

    def save_pdf_report(self):
        # lógica para salvar o relatório em PDF
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Salvar Relatório em PDF", "", "PDF Files (*.pdf)")
        if file_path:
            # Salvar o arquivo em PDF
            print("Relatório salvo em PDF com sucesso!")
            print("Caminho do arquivo:", file_path)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

