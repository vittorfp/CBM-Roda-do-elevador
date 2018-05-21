# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CBM-RodaGuia/mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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
        MainWindow.resize(1367, 830)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 0, 731, 61))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 60, 101, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(60, 50, 471, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.crop_borr = QtGui.QGraphicsView(self.centralwidget)
        self.crop_borr.setGeometry(QtCore.QRect(710, 160, 291, 301))
        self.crop_borr.setObjectName(_fromUtf8("crop_borr"))
        self.rachaduras = QtGui.QGraphicsView(self.centralwidget)
        self.rachaduras.setGeometry(QtCore.QRect(1040, 160, 291, 301))
        self.rachaduras.setObjectName(_fromUtf8("rachaduras"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(800, 140, 121, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(1100, 140, 191, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 520, 221, 251))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.progressBar = QtGui.QProgressBar(self.groupBox)
        self.progressBar.setGeometry(QtCore.QRect(30, 80, 161, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(20, 50, 181, 17))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(30, 140, 171, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(70, 140, 231, 20))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.foto_inicial = QtGui.QGraphicsView(self.centralwidget)
        self.foto_inicial.setGeometry(QtCore.QRect(40, 160, 291, 301))
        self.foto_inicial.setObjectName(_fromUtf8("foto_inicial"))
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(480, 140, 101, 17))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.foto_atual = QtGui.QGraphicsView(self.centralwidget)
        self.foto_atual.setGeometry(QtCore.QRect(380, 160, 291, 301))
        self.foto_atual.setObjectName(_fromUtf8("foto_atual"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(710, 520, 201, 80))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(10, 30, 161, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1367, 25))
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
        self.label_4.setText(_translate("MainWindow", "Borracha da roda", None))
        self.label_5.setText(_translate("MainWindow", "Identificação de rachaduras", None))
        self.groupBox.setTitle(_translate("MainWindow", "Parâmetro de CBM", None))
        self.label_6.setText(_translate("MainWindow", "Percentual de rachaduras", None))
        self.label_9.setText(_translate("MainWindow", "Roda dentro da vida útil", None))
        self.label_7.setText(_translate("MainWindow", "Roda no inicio do monitoramento", None))
        self.label_8.setText(_translate("MainWindow", "Imagem atual", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Diagnostico de software", None))
        self.label_3.setText(_translate("MainWindow", "Conexão MQTT OK", None))

