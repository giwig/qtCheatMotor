# -*- coding: utf-8 -*-

import os
import sys
# from pprint import pprint
# from ctypes import c_uint64, c_size_t

# import win32con
# from platinfo import PlatInfo
# from ReadWriteMemory import ReadWriteMemory, Process
# from capstone import *
# from hexdump import hexdump
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QDialog, QTreeWidgetItem, QTableWidgetItem, QListWidgetItem

from inc.dlg_memory_map import MemoryMapDialog
from inc.dlg_process_list import ProcessListDialog
from ui.mainwindow import Ui_MainWindow
from ui.memory_map import Ui_dlgMemoryMap

from inc.process import GWProcess
from inc.process_list import GWProcessList


"""
def find_process(name="UE4Editor.exe") -> Process:
    rwm = ReadWriteMemory()
    ps: Process = None
    try:
        # rwm.get_process_by_name()
        ps = rwm.get_process_by_name(process_name=name)
    except Exception as e:
        print("{}".format(e))
    return ps


def read_memmory(process: Process = None, address: ctypes.c_uint64 = 0x0, buff_len = 0) -> bytes:
    mem_buf     = (ctypes.c_uint8 * buff_len)(0)
    # mem_buf     = ctypes.create_string_buffer(buff_len)
    # mem_buf:    bytes = bytes(b'\x01')*(buff_len)
    bytesRead   = ctypes.c_uint64(0)
    try:
        print("Address == 0x{:X}".format(address.value))
        ctypes.windll.kernel32.ReadProcessMemory(ctypes.c_uint64(process.handle).value, ctypes.c_uint64(address.value), mem_buf, buff_len, ctypes.byref( bytesRead ) )
        print("Bytes readed == 0x{:X}".format(bytesRead.value))
    except Exception as e:
        print("{}".format(e))
    print(hexdump(bytes(mem_buf), address.value))
    ret_buf = bytes(mem_buf)
    return ret_buf


def dism(mem_buf: bytes = None, buff_len: int = 0, address: ctypes.c_uint64 = 0) -> list:
    hexdump(bytes(mem_buf))
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    ret_list: list = list()

    ret = md.disasm(code=bytes(mem_buf), count=buff_len, offset=address)
    for i in ret:
        # print("0x%x:\t%s\t%s" % (i.address, i.mnemonic, i.op_str))
        ret_list.append(i)
    return ret_list

"""


class MainWindow(QMainWindow):

    process: GWProcess = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.binding()

    def binding(self):
        self.ui.actionChoose.triggered.connect(self.on_process_list)
        self.ui.actionMemory_map.triggered.connect(self.on_memory_map_clicked)

    def on_memory_map_clicked(self):
        dlg = MemoryMapDialog(self, self.process)
        dlg.owner = self
        dlg.exec_()

    def on_process_list(self):
        dlg = ProcessListDialog(self)
        dlg.owner = self
        dlg.exec_()
        if dlg.proc is not None:
            self.process = dlg.proc
            self.ui.actionMemory_map.setEnabled(True)
            self.process.memory_enum_from_to()


if __name__ == '__main__':
    os.system("cls")

    """
    rwm: ReadWriteMemory
    ps: Process

    print("Platform == {}".format(PlatInfo().name()))
    print("is Admin {}".format(ctypes.windll.shell32.IsUserAnAdmin()))

    # 0x7FFA503513A0
    # addr: ctypes.c_uint64 = ctypes.c_uint64(0x7FFA503513A0)
    # 0x7FFA5070EB80
    addr: ctypes.c_uint64 = ctypes.c_uint64(0x7FFA503513A0)


    ps = find_process()

    ps.open()
    buffer = read_memmory(ps, addr, buff_len=0x10)
    dd = dism(buffer, buff_len=0x8, address=addr)
    for i in dd:
        i: CsInsn = i
        print("0x%x:\t%s\t%s" % (i.address, i.mnemonic, i.op_str))
        if "jmp" in i.mnemonic:
            # print("New ADRESS == 0x{:X}".format(int(i.op_str, 16)))
            addr2 = ctypes.c_uint64(int(i.op_str, 16))
            print("New ADRESS == 0x{:X}".format( addr2.value ))
            buff2 = read_memmory(process=ps, address=addr2, buff_len=0x100)
            for n in dism(buff2, buff_len=0x100, address=addr2):
                n: CsInsn = n
                print("\t0x%x:\t%s\t%s" % (n.address, n.mnemonic, n.op_str))


    ps.close()
    """

    """
    # import pefile

    p = GWProcessList()
    p.refresh_process_list()
    print("Process count: {} PageSize: {:X} Min: 0x{:X} Max: 0x{:X} CPU's: {}".format(
        p.count,
        p.system_info.dwPageSize,
        p.system_info.lpMinimumApplicationAddress,
        p.system_info.lpMaximumApplicationAddress,
        p.system_info.dwNumberOfProcessors
    ))
    for pe in p.p_list:
        pe: GWProcess   = pe
        read_address    = 0x800000
        if pe.process_read(c_uint64(read_address), c_size_t(0x100)):
            print(pe.get_memdump(in_off=read_address))
        print("PID: {:8X}\tName: {:30}\tRegions: {}".format(pe.get_pid(), pe.pe.szExeFile, len(pe.mem.memory)))
    """


    app = QApplication([])
    application = MainWindow()
    application.show()

    sys.exit(app.exec())



