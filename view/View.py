import sys

import requests
import json

from PySide6.QtWidgets import QLineEdit, QPushButton, QSizePolicy, QWidget, QApplication, \
    QTableWidget,QTableWidgetItem,QAbstractItemView,QMainWindow, QVBoxLayout, QComboBox, QLabel, QMessageBox
#from Pyside6.QWidgets import QMaindWindow, QVBoxLayout, QComboBox, QLabel

from controller.Controller import DataBase
from model.model import Cliente

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(900, 900)

        self.setWindowTitle('Cadastro de Cliente')

        self.lbl_id = QLabel('id')
        self.txt_id = QLineEdit()

        self.lbl_nota = QLabel('Nota:')
        self.txt_nota = QLineEdit()
        self.txt_nota.setFixedHeight(50)  # Define a altura do QLineEdit em pixels

        self.lbl_titulo_nota = QLabel('Titulo da Nota')
        self.txt_titulo_nota = QLineEdit()


        self.btn_salvar = QPushButton('Salvar')
        self.btn_limpar = QPushButton('Limpar')

        self.btn_remover = QPushButton('Remover')
        self.tabela_clientes  = QTableWidget()
        self.tabela_clientes.setColumnCount(3)
        self.tabela_clientes.setHorizontalHeaderLabels(['ID','TITULO_DA_NOTA','NOTA'])
        self.tabela_clientes.setSelectionMode(QAbstractItemView.NoSelection)
        self.tabela_clientes.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)

        layout.addWidget(self.lbl_titulo_nota)
        layout.addWidget(self.txt_titulo_nota)
        layout.addWidget(self.lbl_nota)
        layout.addWidget(self.txt_nota)


        layout.addWidget(self.tabela_clientes)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_limpar)
        layout.addWidget(self.btn_remover)


        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.btn_remover.setVisible(False)
        self.btn_salvar.clicked.connect(self.salvar_cliente)
        self.txt_id.editingFinished.connect(self.conulta_cliente)
        self.btn_limpar.clicked.connect(self.limpar)
        self.tabela_clientes.cellDoubleClicked.connect(self.carrega_dados)
        self.btn_remover.clicked.connect(self.remover_cliente)
        self.popula_tabela_cliente()

    def salvar_cliente(self):
        db = DataBase()

        cliente = Cliente(
            ID=self.txt_id.text(),
            Titulo_da_nota=self.txt_titulo_nota.text(),
            nota=self.txt_nota.text(),
        )

        retorno = db.registrar_cliente(cliente)

        if self.btn_salvar.text() =='Salvar':
            if retorno == 'Ok':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Cadastro Realizado')
                msg.setText('Cadastro Realizado com Sucesso')
                msg.exec()
            elif 'UNIQUE constraint failed:CLIENTE CPF' in retorno[0]:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Cliente ja cadastrado')
                msg.setText(f'O CPF {self.txt_id} Cliente ja esta cadastrado')
                msg.exec()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao cadastrar')
                msg.setText(f'Erro ao cadastrar o cliente, verifique seus dados')
                msg.exec()
                self.limpar()

        if self.btn_salvar.text() == 'Atualizar':
            retorno = db.atualizar_cliente(cliente)

            if retorno == 'OK':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText('Cadastro Atualizado')
                msg.exec()
                self.limpar()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao atualizar')
                msg.setText(f'Erro ao Atualizar o cliente, verifique os dados')
                msg.exec()
        self.popula_tabela_cliente()
        self.txt_id.setReadOnly(False)

    def conulta_cliente(self):
       if str(self.txt_id.text().replace(',','').replace('-','')) != '':
        db = DataBase()
        retorno =  db.consultar_cliente(str(self.txt_id.text().replace(',','').replace('-','')))
        if retorno is not None:
            self.btn_salvar.setText('Atualizar')
            msg = QMessageBox()
            msg.setWindowTitle('Cliente ja Cadastrado!')
            msg.setText(f'O CPF{self.txt_id.text()} já está cadastraado ')
            msg.exec()
            self.txt_titulo_nota.setText(retorno[1])
            self.txt_nota.setText(retorno[2])
            self.btn_remover.setVisible(True)

    def remover_cliente(self):
        msg = QMessageBox()
        msg.setWindowTitle('Remover Cliente')
        msg.setText('Este item será excluído')
        msg.setInformativeText(f'Você deseja remover o cliente de id {self.txt_id.text()}?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText('Sim')
        msg.button(QMessageBox.No).setText('Não')
        resposta = msg.exec()

        if resposta == QMessageBox.Yes:
            db = DataBase()
            if db.deletar_cliente(self.txt_id.text()) == 'OK':
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Remover Cliente')
                nv_msg.setText('Cliente deletado com sucesso!')
                nv_msg.exec()
                self.limpar()
            else:
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Erro ao remover Cliente')
                nv_msg.exec()
        self.txt_id.setReadOnly(False)
        self.popula_tabela_cliente()
    def limpar(self):
        for widget in self.container.children():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
        self.btn_remover.setVisible(False)
        self.btn_salvar.setText('Salvar')
        self.txt_id.setReadOnly(False)
        self.popula_tabela_cliente()

    def popula_tabela_cliente(self):
        self.tabela_clientes.setRowCount(0)
        db = DataBase()
        lista_clientes = db.consultar_todos_clientes()
        self.tabela_clientes.setRowCount(len(lista_clientes))
        for linha, cliente in enumerate(lista_clientes):
            for coluna, valor in enumerate(cliente):
                self.tabela_clientes.setItem(linha, coluna, QTableWidgetItem(str(valor)))

    def carrega_dados(self, row, column):
        self.txt_id.setText(self.tabela_clientes.item(row, 0).text())
        self.txt_titulo_nota.setText(self.tabela_clientes.item(row, 1).text())
        self.txt_nota.setText(self.tabela_clientes.item(row, 2).text())
        self.btn_salvar.setText('Atualizar')
        self.btn_remover.setVisible(True)
        self.txt_id.setReadOnly(True)
