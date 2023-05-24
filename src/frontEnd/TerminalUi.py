from PyQt5 import QtCore, QtGui, QtWidgets
import os


class Ui_Form(object):
    def __init__(self, qProcess, args):
        self.qProcess = qProcess
        self.args = args
        self.iconDir = "../../images"
        # super().__init__()
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1244, 644)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1131, 471))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 35))
        self.progressBar.setStyleSheet("QProgressBar::chunk {\n"
"    background-color: rgb(54,158,225);\n"
"}")
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.redo_simulation_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.redo_simulation_button.setMaximumSize(QtCore.QSize(16777215, 35))
        self.redo_simulation_button.setObjectName("redo_simulation_button")
        self.horizontalLayout.addWidget(self.redo_simulation_button)
        self.cancel_simulation_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cancel_simulation_button.setMaximumSize(QtCore.QSize(16777215, 35))
        self.cancel_simulation_button.setObjectName("cancel_simulation_button")
        self.horizontalLayout.addWidget(self.cancel_simulation_button)
        self.light_dark_mode_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.light_dark_mode_button.sizePolicy().hasHeightForWidth())
        self.light_dark_mode_button.setSizePolicy(sizePolicy)
        self.light_dark_mode_button.setMaximumSize(QtCore.QSize(35, 35))
        self.light_dark_mode_button.setText("")
        self.light_dark_mode_button.setObjectName("light_dark_mode_button")
        self.horizontalLayout.addWidget(self.light_dark_mode_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.simulationConsole = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.simulationConsole.sizePolicy().hasHeightForWidth())
        self.simulationConsole.setSizePolicy(sizePolicy)
        self.simulationConsole.setMinimumSize(QtCore.QSize(0, 400))
        self.simulationConsole.setStyleSheet("QTextEdit {\n"
"    background-color: rgb(36, 31, 49);\n"
"    color: white;\n"
"}")
        self.simulationConsole.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.simulationConsole.setObjectName("simulationConsole")
        self.verticalLayout.addWidget(self.simulationConsole)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.redo_simulation_button.setText(_translate("Form", "Redo Simulation"))
        self.cancel_simulation_button.setText(_translate("Form", "Cancel Simulation"))
        self.simulationConsole.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The quick brown fox jumped over the lazy dog</p></body></html>"))

        self.simulationConsole.setText("")

        self.dark_color = True
        self.light_dark_mode_button.setIcon(QtGui.QIcon(os.path.join(self.iconDir, 'light_mode.png')))
        self.light_dark_mode_button.clicked.connect(self.changeColor)

        self.cancel_simulation_button.clicked.connect(self.cancelSimulation)
        self.redo_simulation_button.clicked.connect(self.redoSimulation)

    def writeSimulationStatusToConsole(self, isSuccess):
        failedFormat = '<span style="color:#ff3333;">{}</span>'
        successFormat = '<span style="color:#00ff00;">{}</span>'

        if self.qProcess.exitStatus() == QtCore.QProcess.NormalExit:
            if isSuccess:
                self.simulationConsole.append(successFormat.format("Simulation Completed Successfully!"))
            else:
                self.simulationConsole.append(failedFormat.format("Simulation Failed!"))
    
    def showProgressCompleted(self):
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 100)

    def cancelSimulation(self):
        if (self.qProcess.state() == QtCore.QProcess.NotRunning):
            return
        cancelFormat = '<span style="color:#3385ff;">{}</span>'
        self.qProcess.kill()
        
        #To show progressBar completed
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 100)

        self.simulationConsole.append(cancelFormat.format("Simulation Cancelled!"))
        self.simulationConsole.verticalScrollBar().setValue(
            self.simulationConsole.verticalScrollBar().maximum()
        )

    def redoSimulation(self):
        if (self.qProcess.state() == QtCore.QProcess.Running):
            return
        
        #To make the progressbar running
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)

        self.simulationConsole.setText("")
        self.qProcess.start('ngspice', self.args)

    def changeColor(self):
        if self.dark_color is True:
            self.simulationConsole.setStyleSheet("QTextEdit {\n"
            "    background-color: white;\n"
            "    color: black;\n"
            "}")
            self.light_dark_mode_button.setIcon(QtGui.QIcon(os.path.join(self.iconDir, "dark_mode.png")))
            self.dark_color = False
        else:
            self.simulationConsole.setStyleSheet("QTextEdit {\n"
            "    background-color: rgb(36, 31, 49);\n"
            "    color: white;\n"
            "}")
            self.light_dark_mode_button.setIcon(QtGui.QIcon(os.path.join(self.iconDir, "light_mode.png")))
            self.dark_color = True