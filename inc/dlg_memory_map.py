# -*- coding: utf-8 -*-

from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem

from inc.process import GWProcess
from ui.memory_map import Ui_dlgMemoryMap


class MemoryMapDialog(QDialog):

    proc: GWProcess = None

    def __init__(self, parent=None, proc: GWProcess = None):
        super(MemoryMapDialog, self).__init__(parent)
        self.ui = Ui_dlgMemoryMap()
        self.ui.setupUi(self)
        self.ui.treeWidget.setHeaderLabels(['BASE_ADDRESS', 'SIZE', 'PROTECT'])
        if proc is not None:
            self.proc = proc

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        print("Count: {}".format(
            len(self.proc.mem.memory)
        ))

        for m in self.proc.mem.memory.keys():
            size = self.proc.mem.memory[m].RegionSize
            prot = self.proc.mem.memory[m].Protect
            # print(m)
            item = QTreeWidgetItem(["0x{:X}".format(m), "{:X}".format(size), "{:08X}".format(prot)])
            # item.addChild(QTreeWidgetItem([m, "LOLO", "LULU"]))
            self.ui.treeWidget.addTopLevelItem(item)
        self.ui.treeWidget.setColumnWidth(0, 150)
        self.ui.lblInfo.setText("Count: {}    Size: {}".format(self.proc.mem.count, self.proc.mem.get_size_in_byte()))




