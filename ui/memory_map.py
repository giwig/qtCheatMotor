# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'memory_map.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dlgMemoryMap(object):
    def setupUi(self, dlgMemoryMap):
        dlgMemoryMap.setObjectName("dlgMemoryMap")
        dlgMemoryMap.resize(673, 447)
        self.verticalLayout = QtWidgets.QVBoxLayout(dlgMemoryMap)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget = QtWidgets.QTreeWidget(dlgMemoryMap)
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.treeWidget.setFont(font)
        self.treeWidget.setColumnCount(3)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.treeWidget.headerItem().setText(1, "2")
        self.treeWidget.headerItem().setText(2, "3")
        self.verticalLayout.addWidget(self.treeWidget)
        self.gboxInfo = QtWidgets.QGroupBox(dlgMemoryMap)
        self.gboxInfo.setObjectName("gboxInfo")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.gboxInfo)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblInfo = QtWidgets.QLabel(self.gboxInfo)
        self.lblInfo.setObjectName("lblInfo")
        self.horizontalLayout.addWidget(self.lblInfo)
        self.verticalLayout.addWidget(self.gboxInfo)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlgMemoryMap)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(dlgMemoryMap)
        self.buttonBox.accepted.connect(dlgMemoryMap.accept)
        self.buttonBox.rejected.connect(dlgMemoryMap.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgMemoryMap)

    def retranslateUi(self, dlgMemoryMap):
        _translate = QtCore.QCoreApplication.translate
        dlgMemoryMap.setWindowTitle(_translate("dlgMemoryMap", "Dialog"))
        self.gboxInfo.setTitle(_translate("dlgMemoryMap", "Info"))
        self.lblInfo.setText(_translate("dlgMemoryMap", "TextLabel"))
