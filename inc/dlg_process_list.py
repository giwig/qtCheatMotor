# -*- coding: utf-8 -*-

from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QListWidgetItem

from inc.process_list import GWProcessList
from ui.process_list import Ui_dlgProcessList
from inc.process import GWProcess


class ProcessListDialog(QDialog):

    proc: GWProcess = None

    def __init__(self, parent=None):
        super(ProcessListDialog, self).__init__(parent)
        self.ui = Ui_dlgProcessList()
        self.ui.setupUi(self)
        self.procs: GWProcessList = GWProcessList()
        self.procs.refresh_process_list()
        self.ui.listWidget.itemClicked.connect(self.on_item_clicked)
        self.ui.listWidget.itemDoubleClicked.connect(self.on_item_dbl_click)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        names = []
        for p in self.procs.p_list:
            p: GWProcess = p
            names.append(p.get_name())
        self.ui.listWidget.addItems(names)

    def on_item_clicked(self, item: QListWidgetItem):
        print(item.text())
        for p in self.procs.p_list:
            p: GWProcess = p
            if p.get_name() == item.text():
                self.proc = p
                self.setWindowTitle(p.get_name())
                self.owner.statusBar().showMessage("{:7}   {}".format(p.get_pid(), p.get_name() ))

    def on_item_dbl_click(self, item: QListWidgetItem):
        self.on_item_clicked(item)
        self.close()

    def close(self) -> bool:
        super(ProcessListDialog, self).close()



