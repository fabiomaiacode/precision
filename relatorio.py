from datetime import date
import tempfile
import subprocess
import win32print
import win32api
import pandas as pd
import os
import sqlite3
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QDialog, QPushButton, \
    QFileDialog, QWidget, QStackedWidget, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt6.QtGui import QIcon, QPainter, QTextDocument, QPageSize, QPageLayout
from PyQt6.QtCore import QDate, QSize, Qt, QFileDevice, QSizeF, QRectF
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import sys
from fpdf import FPDF


class RelatorioWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.title_label = QLabel("RELATÓRIO")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.generate_button = QPushButton("Gerar Relatório")
        self.generate_button.clicked.connect(self.generate_report)

        self.update_button = QPushButton("Atualizar Tabela")
        self.update_button.clicked.connect(self.update_table)
        self.update_button.setEnabled(False)

        self.content_label = QLabel()
        self.content_label.setWordWrap(True)
        self.content_label.setVisible(False)

        self.save_pdf_button = QPushButton()
        self.save_pdf_button.setIcon(QIcon("save_pdf.png"))  # Define a imagem do botão
        self.save_pdf_button.setIconSize(QSize(100, 100))  # Define o tamanho do ícone
        self.save_pdf_button.setMaximumSize(100, 100)  # Define o tamanho do botão
        self.save_pdf_button.setFlat(True)  # Remove o efeito de botão retangular
        self.save_pdf_button.clicked.connect(self.save_pdf_report)
        self.save_pdf_button.setVisible(False)

        self.print_button = QPushButton()
        self.print_button.setIcon(QIcon("print.png"))  # Define a imagem do botão
        self.print_button.setIconSize(QSize(100, 100))  # Define o tamanho do ícone
        self.print_button.setMaximumSize(100, 100)  # Define o tamanho do botão
        self.print_button.setFlat(True)  # Remove o efeito de botão retangular
        self.print_button.clicked.connect(self.print_report)
        self.print_button.setVisible(False)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Código", "Nome", "Categoria", "Quantidade"])

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_pdf_button)
        self.button_layout.addWidget(self.print_button)
        self.button_layout.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.table)
        layout.addWidget(self.content_label)
        layout.addLayout(self.button_layout)  # Adiciona o layout horizontal com os botões
        layout.setSpacing(20)

        self.setLayout(layout)

    def generate_report(self):
        # Conexão com o banco de dados
        conn = sqlite3.connect('database.db')

        # Cria um cursor para executar comandos SQL
        cursor = conn.cursor()

        # Executa uma consulta para obter os dados da tabela "products"
        cursor.execute("SELECT * FROM products")

        # Obtém todos os registros retornados pela consulta
        table_data = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        conn.close()

        # Cria o DataFrame a partir dos dados
        df = pd.DataFrame(table_data, columns=["ID", "Código", "Nome", "Categoria", "Quantidade"])

        # Converte o DataFrame em uma lista de listas
        table_data = [list(df.columns)] + df.values.tolist()

        # Atualiza a tabela com os dados do relatório
        self.table.setRowCount(len(table_data))
        for i, row in enumerate(table_data):
            for j, item in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(item)))

        self.update_button.setEnabled(True)
        self.save_pdf_button.setVisible(True)
        self.print_button.setVisible(True)

        self.content_label.setText("Relatório gerado com sucesso.")
        self.content_label.setVisible(True)
        
        self.table_data = table_data


    def update_table(self):
        self.generate_report()

    def save_pdf_report(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Relatório em PDF", "", "PDF Files (*.pdf)")

        if file_path:
            # Gera o PDF com os dados do relatório
            pdf = SimpleDocTemplate(
                file_path,
                pagesize=letter,
                leftMargin=20,
                rightMargin=20,
                topMargin=15,
                bottomMargin=30
            )
            elements = []

            # Adiciona as imagens de logotipo
            logo1 = Image("logo.png")
            logo1.drawHeight = 100  # Ajusta a altura da imagem
            logo1.drawWidth = 100   # Ajusta a largura da imagem

            logo2 = Image("logo2.png")
            logo2.drawHeight = 100
            logo2.drawWidth = 100

            # Cria o título
            title_text = "Relatório de Estoque - Gerência de Feiras - Secretaria de Serviços Públicos de Caruaru"
            title_style = ParagraphStyle(
                name="TitleStyle",
                parent=getSampleStyleSheet()["Heading1"],
                fontSize=11,  # Altera o tamanho da fonte para 10
                textColor=colors.black,
                spaceAfter=20,
                alignment=1  # Centraliza o título
            )
            title = Paragraph(title_text, title_style)

            # Cria a tabela para as imagens e o título
            header_table = Table([[logo1, logo2], [title]], colWidths=[250, 250])
            header_table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # Alinha verticalmente no centro
                ("LEFTPADDING", (0, 0), (-1, -1), 0),   # Remove o espaçamento interno à esquerda
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),  # Remove o espaçamento interno à direita
                ("SPAN", (0, 1), (-1, 1)),  # Ocupa todas as colunas na segunda linha (título)
                ("ALIGN", (0, 0), (0, 0), "RIGHT"),  # Alinha a primeira célula à direita
                ("ALIGN", (1, 0), (1, 0), "LEFT"),  # Alinha a segunda célula à esquerda
            ]))

            # Adiciona as imagens e o título ao PDF
            elements.append(header_table)

            # Obtém os dados da tabela
            table_data = []
            header_labels = []
            for column in range(self.table.columnCount()):
                header_labels.append(self.table.horizontalHeaderItem(column).text())

            table_data.append(header_labels)

            table_data = self.table_data

            # Cria a tabela no PDF
            pdf_table = Table(table_data, repeatRows=1)

            # Define o estilo da tabela
            pdf_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Define a cor de fundo do cabeçalho
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),  # Define a cor do texto do cabeçalho
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Define a fonte do cabeçalho em negrito
                ("FONTSIZE", (0, 0), (-1, 0), 10),  # Define o tamanho da fonte do cabeçalho
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),  # Define o espaçamento inferior do cabeçalho
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),  # Define a cor de fundo das células
                ("FONTSIZE", (0, 1), (-1, -1), 10),  # Define o tamanho da fonte das células
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),  # Define a fonte das células
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Alinha o conteúdo das células no centro
                ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Adiciona uma grade nas células
            ]))

            # Adiciona a tabela ao PDF
            elements.append(pdf_table)

            # Gera o documento PDF
            pdf.build(elements)

            self.content_label.setText("Relatório salvo em PDF com sucesso.")
        else:
            self.content_label.setText("Ação de salvar relatório em PDF foi cancelada.")
        self.content_label.setVisible(True)

    def print_report(self):
        styles = getSampleStyleSheet()

        # Define os estilos para o título e os parágrafos de conteúdo
        title_style = ParagraphStyle(
            "TitleStyle",
            parent=styles["Heading1"],
            fontSize=16,
            textColor=colors.black,
            spaceAfter=14,
        )

        content_style = ParagraphStyle(
            "ContentStyle",
            parent=styles["Normal"],
            fontSize=12,
            textColor=colors.black,
            spaceAfter=6,
        )

        # Cria um documento PDF temporário
        with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
            file_path = temp_pdf.name

        # Gera o relatório em PDF
        doc = SimpleDocTemplate(
            file_path, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
        )
        elements = []

        # Adiciona o título
        elements.append(Paragraph("RELATÓRIO", title_style))

        # Adiciona a data atual
        today = date.today().strftime("%d/%m/%Y")
        elements.append(Paragraph(f"Data: {today}", content_style))

        # Adiciona uma tabela com os dados
        table_data = [["ID", "Código", "Nome", "Categoria", "Quantidade"]]

        # Conexão com o banco de dados
        conn = sqlite3.connect("database.db")

        # Cria um cursor para executar comandos SQL
        cursor = conn.cursor()

        # Recupera os dados da tabela
        cursor.execute("SELECT * FROM products")
        data = cursor.fetchall()

        table_data.extend(data)

        # Fecha a conexão com o banco de dados
        conn.close()

        # Define o estilo da tabela
        table_style = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 14),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )

        # Cria a tabela
        table = Table(table_data)
        table.setStyle(table_style)
        elements.append(table)

        # Gera o documento PDF
        doc.build(elements)

        # Obter a impressora padrão
        default_printer = win32print.GetDefaultPrinter()

        # Chama o comando de impressão nativo do sistema com o arquivo PDF temporário
        subprocess.run(["python", "-m", "win32print", "-p", default_printer, file_path])

        # Remove o arquivo PDF temporário
        os.remove(file_path)

    def init_ui(self):
        self.setWindowTitle("Gerador de Relatórios")
        self.setGeometry(200, 200, 800, 600)
        self.show()



    def generate_html_report(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
            body {
                font-family: Arial, sans-serif;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
            }
            th {
                background-color: #808080;
                color: white;
                font-weight: bold;
            }
            </style>
        </head>
        <body>
            <h1>Relatório de Estoque - Gerência de Feiras - Secretaria de Serviços Públicos de Caruaru</h1>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Código</th>
                    <th>Nome</th>
                    <th>Categoria</th>
                    <th>Quantidade</th>
                </tr>
        """

        # Obter os dados da tabela
        table_data = []
        header_labels = []
        for column in range(self.table.columnCount()):
            header_labels.append(self.table.horizontalHeaderItem(column).text())

        table_data.append(header_labels)

        for row in range(self.table.rowCount()):
            row_data = []
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            table_data.append(row_data)

        # Adicionar os dados da tabela à string HTML
        for row in table_data:
            html += "<tr>"
            for item in row:
                html += "<td>{}</td>".format(item)
            html += "</tr>"

        html += """
            </table>
        </body>
        </html>
        """

        return html



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Relatório de Estoque")
        self.setFixedSize(800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.relatorio_widget = RelatorioWidget()
        self.stacked_widget.addWidget(self.relatorio_widget)

        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec()
