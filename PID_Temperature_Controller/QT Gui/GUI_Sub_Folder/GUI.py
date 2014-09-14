# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created: Thu Mar 21 09:46:50 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(808, 612)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setFrameShape(QtGui.QFrame.WinPanel)
        self.scrollArea.setFrameShadow(QtGui.QFrame.Sunken)
        self.scrollArea.setLineWidth(3)
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(-223, -146, 997, 757))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.tempcollection = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.tempcollection.setGeometry(QtCore.QRect(0, 0, 891, 431))
        self.tempcollection.setFrameShape(QtGui.QFrame.StyledPanel)
        self.tempcollection.setFrameShadow(QtGui.QFrame.Raised)
        self.tempcollection.setObjectName(_fromUtf8("tempcollection"))
        self.label = QtGui.QLabel(self.tempcollection)
        self.label.setGeometry(QtCore.QRect(30, 339, 121, 16))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Current Tempreature (C)", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.temperature_plot = MatplotlibWidget(self.tempcollection)
        self.temperature_plot.setGeometry(QtCore.QRect(0, -1, 891, 331))
        self.temperature_plot.setObjectName(_fromUtf8("temperature_plot"))
        self.start_stop_button = QtGui.QPushButton(self.tempcollection)
        self.start_stop_button.setGeometry(QtCore.QRect(460, 360, 391, 31))
        self.start_stop_button.setText(QtGui.QApplication.translate("MainWindow", "Start Temperature Collection", None, QtGui.QApplication.UnicodeUTF8))
        self.start_stop_button.setObjectName(_fromUtf8("start_stop_button"))
        self.current_temp_box = QtGui.QTextBrowser(self.tempcollection)
        self.current_temp_box.setGeometry(QtCore.QRect(10, 359, 151, 31))
        self.current_temp_box.setObjectName(_fromUtf8("current_temp_box"))
        self.label_2 = QtGui.QLabel(self.tempcollection)
        self.label_2.setGeometry(QtCore.QRect(180, 339, 101, 21))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Set Temperature (C)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.set_temp_box = QtGui.QDoubleSpinBox(self.tempcollection)
        self.set_temp_box.setGeometry(QtCore.QRect(180, 360, 131, 31))
        self.set_temp_box.setMaximum(500.0)
        self.set_temp_box.setObjectName(_fromUtf8("set_temp_box"))
        self.set_temp_button = QtGui.QPushButton(self.tempcollection)
        self.set_temp_button.setGeometry(QtCore.QRect(310, 360, 91, 31))
        self.set_temp_button.setText(QtGui.QApplication.translate("MainWindow", "Set Temperature", None, QtGui.QApplication.UnicodeUTF8))
        self.set_temp_button.setObjectName(_fromUtf8("set_temp_button"))
        self.parameters = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.parameters.setGeometry(QtCore.QRect(10, 500, 881, 191))
        self.parameters.setFrameShape(QtGui.QFrame.Box)
        self.parameters.setFrameShadow(QtGui.QFrame.Raised)
        self.parameters.setLineWidth(1)
        self.parameters.setObjectName(_fromUtf8("parameters"))
        self.label_3 = QtGui.QLabel(self.parameters)
        self.label_3.setEnabled(True)
        self.label_3.setGeometry(QtCore.QRect(20, 60, 121, 31))
        self.label_3.setFrameShape(QtGui.QFrame.Box)
        self.label_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_3.setLineWidth(2)
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "         P Parameter", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setScaledContents(False)
        self.label_3.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_12 = QtGui.QLabel(self.parameters)
        self.label_12.setEnabled(True)
        self.label_12.setGeometry(QtCore.QRect(660, 60, 121, 31))
        self.label_12.setFrameShape(QtGui.QFrame.Box)
        self.label_12.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_12.setLineWidth(2)
        self.label_12.setText(QtGui.QApplication.translate("MainWindow", "         Dt Parameter", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setTextFormat(QtCore.Qt.AutoText)
        self.label_12.setScaledContents(False)
        self.label_12.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_4 = QtGui.QLabel(self.parameters)
        self.label_4.setEnabled(True)
        self.label_4.setGeometry(QtCore.QRect(180, 60, 121, 31))
        self.label_4.setFrameShape(QtGui.QFrame.Box)
        self.label_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_4.setLineWidth(2)
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "         I Parameter", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setScaledContents(False)
        self.label_4.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.Dt_box = QtGui.QDoubleSpinBox(self.parameters)
        self.Dt_box.setGeometry(QtCore.QRect(660, 100, 121, 22))
        self.Dt_box.setDecimals(4)
        self.Dt_box.setMinimum(0.001)
        self.Dt_box.setMaximum(10.0)
        self.Dt_box.setSingleStep(0.1)
        self.Dt_box.setObjectName(_fromUtf8("Dt_box"))
        self.P_box = QtGui.QDoubleSpinBox(self.parameters)
        self.P_box.setGeometry(QtCore.QRect(20, 100, 121, 22))
        self.P_box.setDecimals(4)
        self.P_box.setMinimum(-30.0)
        self.P_box.setMaximum(30.0)
        self.P_box.setSingleStep(0.5)
        self.P_box.setObjectName(_fromUtf8("P_box"))
        self.D_box = QtGui.QDoubleSpinBox(self.parameters)
        self.D_box.setGeometry(QtCore.QRect(500, 100, 121, 22))
        self.D_box.setDecimals(4)
        self.D_box.setMinimum(-30.0)
        self.D_box.setMaximum(30.0)
        self.D_box.setSingleStep(0.5)
        self.D_box.setObjectName(_fromUtf8("D_box"))
        self.It_box = QtGui.QDoubleSpinBox(self.parameters)
        self.It_box.setGeometry(QtCore.QRect(340, 100, 121, 22))
        self.It_box.setDecimals(4)
        self.It_box.setMinimum(0.001)
        self.It_box.setMaximum(10.0)
        self.It_box.setSingleStep(0.1)
        self.It_box.setObjectName(_fromUtf8("It_box"))
        self.label_11 = QtGui.QLabel(self.parameters)
        self.label_11.setEnabled(True)
        self.label_11.setGeometry(QtCore.QRect(500, 60, 121, 31))
        self.label_11.setFrameShape(QtGui.QFrame.Box)
        self.label_11.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_11.setLineWidth(2)
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "         D Parameter", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setTextFormat(QtCore.Qt.AutoText)
        self.label_11.setScaledContents(False)
        self.label_11.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.I_box = QtGui.QDoubleSpinBox(self.parameters)
        self.I_box.setGeometry(QtCore.QRect(180, 100, 121, 22))
        self.I_box.setDecimals(4)
        self.I_box.setMinimum(-30.0)
        self.I_box.setMaximum(30.0)
        self.I_box.setSingleStep(0.5)
        self.I_box.setObjectName(_fromUtf8("I_box"))
        self.label_5 = QtGui.QLabel(self.parameters)
        self.label_5.setEnabled(True)
        self.label_5.setGeometry(QtCore.QRect(340, 60, 121, 31))
        self.label_5.setFrameShape(QtGui.QFrame.Box)
        self.label_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_5.setLineWidth(2)
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "         It Parameter", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setTextFormat(QtCore.Qt.AutoText)
        self.label_5.setScaledContents(False)
        self.label_5.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_7 = QtGui.QLabel(self.parameters)
        self.label_7.setGeometry(QtCore.QRect(20, 20, 171, 31))
        self.label_7.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_7.setFrameShadow(QtGui.QFrame.Raised)
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "PID Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setMargin(1)
        self.label_7.setIndent(50)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.save_params_button = QtGui.QPushButton(self.parameters)
        self.save_params_button.setGeometry(QtCore.QRect(20, 140, 401, 23))
        self.save_params_button.setText(QtGui.QApplication.translate("MainWindow", "Save Current Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.save_params_button.setObjectName(_fromUtf8("save_params_button"))
        self.save_params_status = QtGui.QTextBrowser(self.parameters)
        self.save_params_status.setGeometry(QtCore.QRect(430, 140, 241, 31))
        self.save_params_status.setObjectName(_fromUtf8("save_params_status"))
        self.connect = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.connect.setGeometry(QtCore.QRect(10, 410, 871, 81))
        self.connect.setFrameShape(QtGui.QFrame.Panel)
        self.connect.setFrameShadow(QtGui.QFrame.Sunken)
        self.connect.setLineWidth(1)
        self.connect.setObjectName(_fromUtf8("connect"))
        self.com_box = QtGui.QComboBox(self.connect)
        self.com_box.setGeometry(QtCore.QRect(290, 30, 91, 22))
        self.com_box.setObjectName(_fromUtf8("com_box"))
        self.connected_result = QtGui.QTextBrowser(self.connect)
        self.connected_result.setGeometry(QtCore.QRect(400, 30, 181, 31))
        self.connected_result.setObjectName(_fromUtf8("connected_result"))
        self.connect_disconnect_button = QtGui.QPushButton(self.connect)
        self.connect_disconnect_button.setGeometry(QtCore.QRect(610, 30, 241, 31))
        self.connect_disconnect_button.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.connect_disconnect_button.setObjectName(_fromUtf8("connect_disconnect_button"))
        self.label_6 = QtGui.QLabel(self.connect)
        self.label_6.setGeometry(QtCore.QRect(10, 20, 161, 51))
        self.label_6.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_6.setFrameShadow(QtGui.QFrame.Raised)
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Connect to Arduino", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_8 = QtGui.QLabel(self.connect)
        self.label_8.setGeometry(QtCore.QRect(300, 10, 91, 20))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Choose COM", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.search_button = QtGui.QPushButton(self.connect)
        self.search_button.setGeometry(QtCore.QRect(184, 30, 91, 21))
        self.search_button.setText(QtGui.QApplication.translate("MainWindow", "Search for COMS", None, QtGui.QApplication.UnicodeUTF8))
        self.search_button.setObjectName(_fromUtf8("search_button"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 808, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

from matplotlibwidget import MatplotlibWidget