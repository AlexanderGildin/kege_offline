# Form implementation generated from reading ui file 'QtRedactor.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from datetime import date


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 990)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.dataTextEdit = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.dataTextEdit.setGeometry(QtCore.QRect(13, 10, 1457, 770))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.dataTextEdit.setFont(font)
        self.dataTextEdit.setObjectName("dataTextEdit")
        self.add_quest = QtWidgets.QPushButton(parent=self.centralwidget)
        self.add_quest.setGeometry(QtCore.QRect(12, 925, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.add_quest.setFont(font)
        self.add_quest.setObjectName("add_quest")
        self.insert_into_db = QtWidgets.QPushButton(parent=self.centralwidget)
        self.insert_into_db.setGeometry(QtCore.QRect(900, 925, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.insert_into_db.setFont(font)
        self.insert_into_db.setObjectName("insert_into_db")
        self.logsTextEdit = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.logsTextEdit.setGeometry(QtCore.QRect(13, 787, 1457, 130))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.logsTextEdit.setFont(font)
        self.logsTextEdit.setObjectName("logsTextEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.dataTextEdit.setPlainText(_translate("MainWindow", "COUNT_OF_QUESTIONS=27\n"
                                                                "MAXTIME=0\n"
                                                                "KEY=password\n"
                                                                f"DESCRIPTION={self.getting_the_date()}\n"
                                                                "I 1730\n"
                                                                "IMG=\n"
                                                                "Q1 1730\n"
                                                                "IMG=\n"
                                                                "FILES=\n"
                                                                "SANS=1, 1\n"
                                                                "SEP=;\n"
                                                                "ANSW=\n"
                                                                "POINTS="))
        self.add_quest.setText(_translate("MainWindow", "Добавить вопрос"))
        #  self.add_info_scr.setText(_translate("MainWindow", "Добавить информационный экран"))
        #  self.check_file.setText(_translate("MainWindow", "Проверить текущий файл"))
        self.insert_into_db.setText(_translate("MainWindow", "Сформировать тест"))
        self.logsTextEdit.setPlainText(_translate("MainWindow", "Лог:"))

    def getting_the_date(self):
        today = date.today()
        self.today_1 = str(today.day) + '_' + str(today.month) + '_' + str(today.year) + '_1'
        return self.today_1
