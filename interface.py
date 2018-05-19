# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CBM-RodaGuia/mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(812, 714)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 0, 371, 61))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 70, 101, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(60, 50, 371, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.foto_atual = QtGui.QGraphicsView(self.centralwidget)
        self.foto_atual.setGeometry(QtCore.QRect(50, 180, 201, 221))
        self.foto_atual.setObjectName(_fromUtf8("foto_atual"))
        self.crop_borr = QtGui.QGraphicsView(self.centralwidget)
        self.crop_borr.setGeometry(QtCore.QRect(280, 180, 201, 221))
        self.crop_borr.setObjectName(_fromUtf8("crop_borr"))
        self.rachaduras = QtGui.QGraphicsView(self.centralwidget)
        self.rachaduras.setGeometry(QtCore.QRect(510, 180, 201, 221))
        self.rachaduras.setObjectName(_fromUtf8("rachaduras"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(100, 160, 101, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(320, 160, 121, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(520, 160, 191, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(510, 420, 221, 121))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.progressBar = QtGui.QProgressBar(self.groupBox)
        self.progressBar.setGeometry(QtCore.QRect(30, 80, 161, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(20, 50, 171, 17))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(100, 430, 111, 17))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.foto_inicial = QtGui.QGraphicsView(self.centralwidget)
        self.foto_inicial.setGeometry(QtCore.QRect(50, 450, 201, 221))
        self.foto_inicial.setObjectName(_fromUtf8("foto_inicial"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 812, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Monitoramento por visão", None))
        self.label.setText(_translate("MainWindow", "CBM - Roda guia", None))
        self.label_2.setText(_translate("MainWindow", "Elevador TQ7", None))
        self.label_3.setText(_translate("MainWindow", "Imagem atual", None))
        self.label_4.setText(_translate("MainWindow", "Borracha da roda", None))
        self.label_5.setText(_translate("MainWindow", "Identificação de rachaduras", None))
        self.groupBox.setTitle(_translate("MainWindow", "Parâmetro de CBM", None))
        self.label_6.setText(_translate("MainWindow", "Percentual de rachaduras", None))
        self.label_7.setText(_translate("MainWindow", "Imagem inicial", None))

