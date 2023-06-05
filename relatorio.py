from datetime import date
import tempfile
import pandas as pd
import os
import sqlite3
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QPushButton, QToolBar, QFileDialog, QWidget, QStackedWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QDate, QSize
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter



class RelatorioWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.title_label = QLabel("RELATÓRIO")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.generate_button = QPushButton("Gerar Relatório")
        self.generate_button.clicked.connect(self.generate_report)

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

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.content_label)
        layout.addWidget(self.save_pdf_button)
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
        df = pd.DataFrame(table_data, columns=["id", "code", "name", "category", "quantity"])

        # Converte o DataFrame em uma lista de listas
        table_data = [list(df.columns)] + df.values.tolist()

        # Define o caminho do arquivo PDF
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Relatório", "", "PDF Files (*.pdf)")

        if file_path:
            # Gera o PDF com os dados do relatório
            pdf = SimpleDocTemplate(file_path, pagesize=letter)
            elements = []

            ## Título do Relatório
            title_style = ParagraphStyle(
                name="TitleStyle",
                parent=getSampleStyleSheet()["Heading1"],
                fontSize=16,
                textColor=colors.black,
                spaceAfter=20,
            )
            title_text = "Relatório de Estoque - Gerência de Feiras - Secretaria de Serviços Públicos de Caruaru"
            title = Paragraph(title_text, title_style)
            elements.append(title)


            # Adiciona as imagens de logotipo
            logo1 = Image("logo.png")
            logo1.drawHeight = 100  # Ajusta a altura da imagem
            logo1.drawWidth = 100   # Ajusta a largura da imagem

            logo2 = Image("logo2.png")
            logo2.drawHeight = 100
            logo2.drawWidth = 100

            # Cria um spacer horizontal entre as imagens
            spacer = Spacer(20, 100)  # Ajuste os valores de acordo com a necessidade

            # Cria a tabela para o cabeçalho
            header_table = Table([[logo1, spacer, logo2]], colWidths=[100, 20, 100])
            header_table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # Alinha verticalmente no centro
                ("LEFTPADDING", (0, 0), (-1, -1), 0),   # Remove o espaçamento interno à esquerda
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),  # Remove o espaçamento interno à direita
            ]))

            # Adiciona o cabeçalho
            elements.append(header_table)

            # Define o estilo da tabela
            style = TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.black),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black)
            ])

            # Cria a tabela e aplica o estilo
            table = Table(table_data, style=style)

            # Adiciona a tabela aos elementos do PDF
            elements.append(table)

            # Adiciona o rodapé
            footer_style = getSampleStyleSheet()["BodyText"]
            footer_text = "Gerado em: {date}".format(date=date.today().strftime("%d/%m/%Y"))
            footer = Paragraph(footer_text, footer_style)
            elements.append(footer)

            # Constrói o PDF
            pdf.build(elements)

            temp_file_path = os.path.join(tempfile.gettempdir(), "temp_report.pdf")

            # Copia o arquivo PDF gerado para o novo caminho
            os.replace(file_path, temp_file_path)

            self.content_label.setText("Relatório gerado com sucesso.")
            self.content_label.setVisible(True)
            self.save_pdf_button.setVisible(True)
        else:
            self.content_label.setText("Geração do relatório cancelada.")
            self.content_label.setVisible(True)
            self.save_pdf_button.setVisible(False)

    def save_pdf_report(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Relatório em PDF", "", "PDF Files (*.pdf)")

        if file_path:
            temp_file_path = os.path.join(tempfile.gettempdir(), "temp_report.pdf")

            # Copia o arquivo PDF gerado para o novo caminho
            os.replace(temp_file_path, file_path)

            self.content_label.setText("Relatório salvo com sucesso.")
        else:
            self.content_label.setText("Salvamento do relatório cancelado.")

        self.content_label.setVisible(True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AF Software")
        self.setGeometry(300, 200, 400, 300)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.relatorio_widget = RelatorioWidget()
        self.central_widget.addWidget(self.relatorio_widget)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    relatorio_widget = RelatorioWidget()
    main_window.setCentralWidget(relatorio_widget)
    main_window.show()
    sys.exit(app.exec())
