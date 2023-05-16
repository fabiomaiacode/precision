from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class AddProductWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastrar Produto")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.createForm()

    def createForm(self):
        self.nameLabel = QLabel("Nome do Produto:")
        self.nameLineEdit = QLineEdit()
        self.layout.addWidget(self.nameLabel)
        self.layout.addWidget(self.nameLineEdit)

        self.codeLabel = QLabel("Código do Produto:")
        self.codeLineEdit = QLineEdit()
        self.layout.addWidget(self.codeLabel)
        self.layout.addWidget(self.codeLineEdit)

        self.addButton = QPushButton("Cadastrar")
        self.layout.addWidget(self.addButton)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Controle de Estoque")
        self.setWindowState(Qt.WindowState.WindowMaximized)
        self.createLayout()
        self.welcomeIndex = 0  # índice do conteúdo da tela inicial

    def createLayout(self):
        # Menu lateral
        menu = QVBoxLayout()

        logo = QLabel()
        pixmap = QPixmap("logo.png").scaled(180, 180)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu.addWidget(logo)

        addBtn = QPushButton("Cadastrar Produto")
        remBtn = QPushButton("Excluir Produto")
        inBtn = QPushButton("Entrada")
        outBtn = QPushButton("Saída")
        rptBtn = QPushButton("Relatório")

        menu.addWidget(addBtn)
        menu.addWidget(remBtn)
        menu.addWidget(inBtn)
        menu.addWidget(outBtn)
        menu.addWidget(rptBtn)

        # Conteúdo
        self.content = QStackedWidget()  # Make it an instance variable

        welcomeContent = QLabel("Bem vindo ao AF Software!\nO software que trata da Gestão de Estoque da \nGerência de Feiras da Secretaria de Serviços Públicos de Caruaru-PE")
        font = welcomeContent.font()  # Obter a fonte atual
        font.setPointSize(16)  # Definir o tamanho da fonte desejado
        welcomeContent.setFont(font)  # Aplicar a nova fonte
        welcomeContent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcomeLayout = QHBoxLayout()
        welcomeLayout.addWidget(welcomeContent)
        welcomeLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcomeWidget = QWidget()
        welcomeWidget.setLayout(welcomeLayout)

        addContent = AddProductWidget()
        remContent = QLabel("Conteúdo do botão Excluir Produto")
        inContent = QLabel("Conteúdo do botão Entrada")
        outContent = QLabel("Conteúdo do botão Saída")
        rptContent = QLabel("Conteúdo do botão Relatório")

        self.content.addWidget(welcomeContent)
        self.content.addWidget(addContent)
        self.content.addWidget(remContent)
        self.content.addWidget(inContent)
        self.content.addWidget(outContent)
        self.content.addWidget(rptContent)

        # Set layout alignment to center for each content widget
        addContent.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        remContent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inContent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outContent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rptContent.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.content.addWidget(welcomeWidget)
        self.content.addWidget(addContent)
        self.content.addWidget(remContent)
        self.content.addWidget(inContent)
        self.content.addWidget(outContent)
        self.content.addWidget(rptContent)

                # Layout principal
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(menu)
        mainLayout.addWidget(self.content)
        self.setLayout(mainLayout)

        # Conexão dos botões
        addBtn.clicked.connect(lambda: self.content.setCurrentWidget(addContent))
        remBtn.clicked.connect(lambda: self.content.setCurrentWidget(remContent))
        inBtn.clicked.connect(lambda: self.content.setCurrentWidget(inContent))
        outBtn.clicked.connect(lambda: self.content.setCurrentWidget(outContent))
        rptBtn.clicked.connect(lambda: self.content.setCurrentWidget(rptContent))
        logo.mousePressEvent = self.showWelcomeContent  # Conexão do logo

        # Propriedades da janela
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint)
        self.showMaximized()

    def showWelcomeContent(self, event):
        # Define o índice do conteúdo da tela inicial e atualiza o QStackedWidget
        self.welcomeIndex = 0
        self.content.setCurrentIndex(self.welcomeIndex)


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    ex.show()
    app.exec()
