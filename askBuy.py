# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'askBuy.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(604, 187)
        self.no = QtWidgets.QPushButton(Form)
        self.no.setGeometry(QtCore.QRect(440, 120, 111, 41))
        self.no.setObjectName("no")
        self.askAniamals = QtWidgets.QLabel(Form)
        self.askAniamals.setGeometry(QtCore.QRect(50, 20, 541, 81))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.askAniamals.setFont(font)
        self.askAniamals.setObjectName("askAniamals")
        self.yes = QtWidgets.QPushButton(Form)
        self.yes.setGeometry(QtCore.QRect(320, 120, 111, 41))
        self.yes.setObjectName("yes")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "askBuy"))
        self.no.setText(_translate("Form", "No"))
        self.askAniamals.setText(_translate("Form", "Would you like to buy a ticket for yourself?"))
        self.yes.setText(_translate("Form", "Yes"))
