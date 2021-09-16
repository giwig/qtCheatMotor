# -*- coding: utf-8 -*-

from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog

from inc.process import GWProcess
from ui.memory_map import Ui_dlgMemoryMap


class MemoryMapDialog(QDialog):

    proc: GWProcess = None

    def __init__(self, parent=None, proc: GWProcess = None):
        super(MemoryMapDialog, self).__init__(parent)
        self.ui = Ui_dlgMemoryMap()
        self.ui.setupUi(self)
        if proc is not None:
            self.proc = proc

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        print("Count: {}".format(
            len(self.proc.mem.memory)
        ))


