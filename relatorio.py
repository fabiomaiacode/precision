import sqlite3
from datetime import date
import pdfkit
from PyQt6.QtWidgets import QMainWindow, QWidget, QGraphicsBlurEffect, QGraphicsEffect, \
      QGraphicsDropShadowEffect, QVBoxLayout, QLabel, QSizePolicy, QSpacerItem, QHBoxLayout, \
          QPushButton, QToolBar, QFileDialog, QTableView, QApplication
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem, QFont, QPainter, QPainterPath,\
    QColor
from PyQt6.QtCore import Qt, QSize, QRect, QDate, QPoint, QEvent
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter, QPrinterInfo, QAbstractPrintDialog



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

        button_layout = QHBoxLayout()  # Layout horizontal para os botões

        self.print_button = QPushButton()
        self.print_button.setIcon(QIcon("print.png"))  # Define a imagem do botão
        self.print_button.setIconSize(QSize(100, 100))  # Define o tamanho do ícone
        self.print_button.setMaximumSize(100, 100)  # Define o tamanho do botão
        self.print_button.setFlat(True)  # Remove o efeito de botão retangular
        self.print_button.installEventFilter(self)  # Instala o filtro de eventos
        self.add_button_shadow_effect(self.print_button)  # Adiciona o efeito de sombra inicialmente
        self.print_button.clicked.connect(self.print_report)

        self.save_pdf_button = QPushButton()
        self.save_pdf_button.setIcon(QIcon("save_pdf.png"))  # Define a imagem do botão
        self.save_pdf_button.setIconSize(QSize(100, 100))  # Define o tamanho do ícone
        self.save_pdf_button.setMaximumSize(100, 100)  # Define o tamanho do botão
        self.save_pdf_button.setFlat(True)  # Remove o efeito de botão retangular
        self.save_pdf_button.installEventFilter(self)  # Instala o filtro de eventos
        self.add_button_shadow_effect(self.save_pdf_button)  # Adiciona o efeito de sombra inicialmente
        self.save_pdf_button.clicked.connect(self.save_pdf_report)

        button_layout.addWidget(self.print_button)
        button_layout.addWidget(self.save_pdf_button)

        layout.addWidget(title_label)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.report_table)
        layout.addLayout(button_layout)  # Adiciona o layout dos botões

        # Adiciona espaço vertical para empurrar o conteúdo para baixo
        spacer_item = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer_item)

    def add_button_shadow_effect(self, button):
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setColor(QColor(0, 0, 0, 250))
        shadow_effect.setOffset(0, 0)
        shadow_effect.setBlurRadius(25)
        button.setGraphicsEffect(shadow_effect)

    def eventFilter(self, obj, event):
        if obj == self.print_button or obj == self.save_pdf_button:
            if event.type() == QEvent.Type.Enter:
                self.add_button_shadow_effect(obj)
            elif event.type() == QEvent.Type.Leave:
                self.remove_button_shadow_effect(obj)
        return super().eventFilter(obj, event)

    def remove_button_shadow_effect(self, button):
        button.setGraphicsEffect(None)

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

        self.save_pdf_button.setVisible(True)


    def save_pdf_report(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Relatório em PDF", "", "PDF Files (*.pdf)")

        if file_path:
            # Salvar o arquivo em PDF
            printer = QPrinter(QPrinterInfo.defaultPrinter())
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_path)

            painter = QPainter()
            painter.begin(printer)
            page_rect = printer.pageRect(QPrinter.Unit.Point)  # Obter o retângulo da página em pontos
            page_size = QSize(int(page_rect.width()), int(page_rect.height()))  # Criar um objeto QSize com largura e altura

            # Definir título do relatório
            title_font = QFont("Arial", 16, QFont.Weight.Bold)
            painter.setFont(title_font)
            title_text = "Relatório de Estoque - Gerência de Feiras - Secretaria de Serviços Públicos - Prefeitura de Caruaru"
            title_width = painter.fontMetrics().boundingRect(QRect(0, 0, page_size.width(), page_size.height()), Qt.AlignmentFlag.AlignCenter, title_text).width()
            title_pos = QPoint(int((page_size.width() - title_width) / 2), 30)
            painter.drawText(title_pos, title_text)

            # Definir rodapé com a data de emissão
            footer_font = QFont("Arial", 12)
            painter.setFont(footer_font)
            footer_text = "Data de emissão: {}".format(QDate.currentDate().toString("dd/MM/yyyy"))
            footer_width = painter.fontMetrics().boundingRect(QRect(0, 0, page_size.width(), page_size.height()), Qt.AlignmentFlag.AlignCenter, footer_text).width()
            footer_pos = QPoint(int((page_size.width() - footer_width) / 2), page_size.height() - 50)
            painter.drawText(footer_pos, footer_text)

            # Posicionar a tabela entre o cabeçalho e o rodapé
            table_height = page_size.height() - title_pos.y() - title_font.pointSize() - 20 - footer_font.pointSize() - 20
            table_pos = QPoint(20, title_pos.y() + title_font.pointSize() + 20)
            self.report_table.setGeometry(table_pos.x(), table_pos.y(), page_size.width() - 40, table_height)

            self.report_table.render(painter)
            painter.end()

            print("Relatório salvo em PDF com sucesso!")
            print("Caminho do arquivo:", file_path)


    def print_report(self):
        # lógica para imprimir o relatório
        printer = QPrinter(QPrinterInfo.defaultPrinter())
        dialog = QPrintDialog(printer, self)

        if dialog.exec() == QAbstractPrintDialog.DialogCode.Accepted:
            painter = QPainter()
            painter.begin(printer)
            page_rect = printer.pageRect(QPrinter.Unit.Point)  # Obter o retângulo da página em pontos
            page_size = QSize(int(page_rect.width()), int(page_rect.height()))  # Criar um objeto QSize com largura e altura

            # Definir título do relatório
            title_font = QFont("Arial", 16, QFont.Weight.Bold)
            painter.setFont(title_font)
            title_text = "Relatório de Estoque - Gerência de Feiras - Secretaria de Serviços Públicos - Prefeitura de Caruaru"
            title_width = painter.fontMetrics().boundingRect(QRect(0, 0, page_size.width(), page_size.height()), Qt.AlignmentFlag.AlignCenter, title_text).width()
            title_pos = QPoint(int((page_size.width() - title_width) / 2), 30)
            painter.drawText(title_pos, title_text)

            # Definir rodapé com a data de emissão
            footer_font = QFont("Arial", 12)
            painter.setFont(footer_font)
            footer_text = "Data de emissão: {}".format(QDate.currentDate().toString("dd/MM/yyyy"))
            footer_width = painter.fontMetrics().boundingRect(QRect(0, 0, page_size.width(), page_size.height()), Qt.AlignmentFlag.AlignCenter, footer_text).width()
            footer_pos = QPoint(int((page_size.width() - footer_width) / 2), page_size.height() - 50)
            painter.drawText(footer_pos, footer_text)

            # Posicionar a tabela entre o cabeçalho e o rodapé
            table_height = page_size.height() - title_pos.y() - title_font.pointSize() - 20 - footer_font.pointSize() - 20
            table_pos = QPoint(20, title_pos.y() + title_font.pointSize() + 20)
            self.report_table.setGeometry(table_pos.x(), table_pos.y(), page_size.width() - 40, table_height)

            self.report_table.render(painter)
            painter.end()

            print("Relatório impresso com sucesso!")



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

        self.create_buttons()
        layout.addLayout(self.button_layout)

    def create_toolbar(self):
        self.toolbar = QToolBar(self)
        self.addToolBar(self.toolbar)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    relatorio_widget = RelatorioWidget()
    main_window.setCentralWidget(relatorio_widget)
    main_window.show()
    sys.exit(app.exec())