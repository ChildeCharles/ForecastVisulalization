# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 860)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1281, 871))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(15, 15, 15, 15)
        self.gridLayout.setObjectName("gridLayout")
        self.city_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.city_label.setObjectName("city_label")
        self.gridLayout.addWidget(self.city_label, 0, 0, 1, 1)
        self.city_input = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.city_input.sizePolicy().hasHeightForWidth())
        self.city_input.setSizePolicy(sizePolicy)
        self.city_input.setObjectName("city_input")
        self.gridLayout.addWidget(self.city_input, 0, 1, 1, 1)
        self.date_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.date_label.setObjectName("date_label")
        self.gridLayout.addWidget(self.date_label, 1, 0, 1, 1)
        self.date_input = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.date_input.setObjectName("date_input")
        self.gridLayout.addWidget(self.date_input, 1, 1, 1, 1)
        self.apply_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.apply_button.setObjectName("apply_button")
        self.gridLayout.addWidget(self.apply_button, 1, 2, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_3d = QtWidgets.QWidget(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3d.sizePolicy().hasHeightForWidth())
        self.widget_3d.setSizePolicy(sizePolicy)
        self.widget_3d.setObjectName("widget_3d")
        self.verticalLayout.addWidget(self.widget_3d)
        self.gridLayout.addLayout(self.verticalLayout, 2, 2, 1, 2)
        self.widget_2d = QtWidgets.QWidget(self.gridLayoutWidget)
        self.widget_2d.setObjectName("widget_2d")
        self.gridLayout.addWidget(self.widget_2d, 2, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Forecast Visualization"))
        self.city_label.setText(_translate("MainWindow", "Select city:"))
        self.date_label.setText(_translate("MainWindow", "Select date:"))
        self.apply_button.setText(_translate("MainWindow", "Apply"))

