# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'animalsYes.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(477, 378)
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(10, 10, 331, 41))
        self.comboBox.setObjectName("comboBox")
        self.add = QtWidgets.QPushButton(Form)
        self.add.setGeometry(QtCore.QRect(370, 10, 81, 41))
        self.add.setObjectName("add")
        self.listLb = QtWidgets.QLabel(Form)
        self.listLb.setGeometry(QtCore.QRect(10, 120, 371, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listLb.setFont(font)
        self.listLb.setObjectName("listLb")
        self.backBt = QtWidgets.QPushButton(Form)
        self.backBt.setGeometry(QtCore.QRect(370, 60, 81, 41))
        self.backBt.setObjectName("backBt")
        self.nextBt = QtWidgets.QPushButton(Form)
        self.nextBt.setGeometry(QtCore.QRect(370, 110, 81, 41))
        self.nextBt.setObjectName("nextBt")
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(10, 170, 441, 192))
        self.listWidget.setObjectName("listWidget")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "animalsYes"))
        self.add.setText(_translate("Form", "Add"))
        self.listLb.setText(_translate("Form", "The list of the animals that will be add to ticket :"))
        self.backBt.setText(_translate("Form", "Go back"))
        self.nextBt.setText(_translate("Form", "Next"))
