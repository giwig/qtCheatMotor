#!/bin/python

from ctypes import c_uint64, windll, c_uint32, c_void_p, c_char, Structure, c_long, c_ulong, POINTER, sizeof, c_size_t, c_wchar, c_int
from inc.process import GWProcess, PROCESSENTRY32W, PROCESSENTRY32A, CloseHandle

TH32CS_INHERIT      = 0x80000000
TH32CS_SNAPHEAPLIST = 0x00000001
TH32CS_SNAPMODULE   = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010
TH32CS_SNAPPROCESS  = 0x00000002
TH32CS_SNAPTHREAD   = 0x00000004
TH32CS_SNAPALL      = TH32CS_SNAPHEAPLIST |  TH32CS_SNAPMODULE | TH32CS_SNAPPROCESS | TH32CS_SNAPTHREAD
MAX_PATH = 260


CreateToolhelp32Snapshot            = windll.kernel32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.reltype    = c_long
CreateToolhelp32Snapshot.argtypes   = [ c_ulong, c_ulong ]


## Process32First
Process32FirstA                     = windll.kernel32.Process32First
Process32FirstA.argtypes            = [ c_void_p, POINTER( PROCESSENTRY32A ) ]
Process32FirstA.rettype             = c_int


## Process32FirstW
Process32FirstW                     = windll.kernel32.Process32FirstW
Process32FirstW.argtypes            = [ c_void_p, POINTER( PROCESSENTRY32W ) ]
Process32FirstW.rettype             = c_int


## Process32Next
Process32NextA                      = windll.kernel32.Process32Next
Process32NextA.argtypes             = [ c_void_p, POINTER(PROCESSENTRY32A) ]
Process32NextA.rettype              = c_int

## Process32NextW
Process32NextW                      = windll.kernel32.Process32NextW
Process32NextW.argtypes             = [ c_void_p, POINTER(PROCESSENTRY32W) ]
Process32NextW.rettype              = c_int


class GWProcesses:

    p_list:     list[GWProcess]     = list()
    hSnap:      POINTER(c_uint64)   = None

    def __init__(self):
        self.clear_process_list()

    def clear_process_list(self):
        if self.p_list is not None:
            self.p_list = list()
            return True
        else:
            return False

    def refresh_process_list(self, in_flags: c_uint32 = TH32CS_SNAPPROCESS, in_pid: c_uint32 = -1) -> bool:
        self.clear_process_list()
        self.hSnap = CreateToolhelp32Snapshot(in_flags, in_pid)
        if self.hSnap == -1:
            return False

        # print("Handle == {}".format(self.hSnap))
        pe64: PROCESSENTRY32W = PROCESSENTRY32W()
        pe64.dwSize = sizeof(pe64)
        if Process32FirstW(self.hSnap, pe64):
            # print("Name == {} PID == {}".format(pe64.szExeFile, pe64.th32ProcessID ))
            self.p_list.append(GWProcess(pe64))
            pe64 = PROCESSENTRY32W()
            pe64.dwSize = sizeof( pe64 )
            while Process32NextW(self.hSnap, pe64):
                # print("Name == {} PID == {}".format(pe64.szExeFile, pe64.th32ProcessID))
                pe64 = PROCESSENTRY32W()
                pe64.dwSize = sizeof(pe64)
                self.p_list.append( GWProcess(pe64) )

        else:
            print("error")

        CloseHandle(self.hSnap)
        return True

