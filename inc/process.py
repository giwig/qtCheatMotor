#!/bin/python

from ctypes import c_uint64, windll, c_uint32, c_void_p, c_char, Structure, c_long, c_ulong, POINTER, sizeof, c_size_t, \
    c_wchar, c_int, c_bool, WinDLL
from ctypes.wintypes import *


import win32api
import win32con
import pywintypes
import win32process
from hexdump import hexdump
from inc.process_memory import GWVirtualMemory

"""
kernel32 = WinDLL('kernel32.dll')

STANDARD_RIGHTS_REQUIRED = 0x000F0000
SYNCHRONIZE = 0x00100000
PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF)

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_CREATE_THREAD = 0x0002
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_MOST = 0x042A

"""
MAX_PATH = 260

# originally just PROCESSENTRY32
class PROCESSENTRY32A(Structure):
    _fields_ = [ ( 'dwSize',                c_ulong ),
                 ( 'cntUsage',              c_ulong),
                 ( 'th32ProcessID',         c_ulong),
                 ( 'th32DefaultHeapID',     c_size_t),
                 ( 'th32ModuleID',          c_ulong),
                 ( 'cntThreads',            c_ulong),
                 ( 'th32ParentProcessID',   c_ulong),
                 ( 'pcPriClassBase',        c_long),
                 ( 'dwFlags',               c_ulong),
                 ( 'szExeFile',             c_char * MAX_PATH ) ]


# c_wchar instead of c_char is the only difference
class PROCESSENTRY32W(Structure):
    _fields_ = [ ( 'dwSize',                c_ulong ),
                 ( 'cntUsage',              c_ulong),
                 ( 'th32ProcessID',         c_ulong),
                 ( 'th32DefaultHeapID',     c_size_t),
                 ( 'th32ModuleID',          c_ulong),
                 ( 'cntThreads',            c_ulong),
                 ( 'th32ParentProcessID',   c_ulong),
                 ( 'pcPriClassBase',        c_long),
                 ( 'dwFlags',               c_ulong),
                 ( 'szExeFile',             c_wchar * MAX_PATH ) ]

## ReadProcessMemory
GWReadProcessMemory                 = windll.kernel32.ReadProcessMemory
GWReadProcessMemory.argtypes        = [ c_void_p, c_void_p, c_void_p, c_size_t, POINTER( c_size_t ) ]
GWReadProcessMemory.rettype         = c_int


## OpenProcess
OpenProcess                         = windll.kernel32.OpenProcess
OpenProcess.argtypes                = [ c_ulong, c_int, c_ulong ]
OpenProcess.rettype                 = c_void_p

## OpenProcess
CloseHandle                         = windll.kernel32.CloseHandle
CloseHandle.argtypes                = [ c_void_p]
CloseHandle.rettype                 = c_int


class GWProcess:

    pe:         PROCESSENTRY32W     = None
    exe_name:   str                 = None
    handle:     c_void_p            = None
    mem_buff                        = None
    file_dir:   str                 = None
    mem:        GWVirtualMemory     = None

    def __init__(self, pe: PROCESSENTRY32W = None):
        if pe:
            self.pe = pe
            self.mem = GWVirtualMemory()
            self.get_dir()

    def set_pe(self, pe: PROCESSENTRY32W = -1):
        self.pe = pe

    def get_pe(self) -> PROCESSENTRY32W:
        return self.pe

    def get_pid(self) -> int:
        return self.pe.th32ProcessID

    def get_memdump(self, in_off = 0) -> str:
        return hexdump(self.mem_buff, off=in_off)

    def memory_information_by_address(self, in_address: c_uint64 = 0):
        if self.process_open(in_access=win32con.PROCESS_QUERY_INFORMATION):
            self.mem.handle_set(self.handle)
            self.mem.get_memory_information_by_address(in_address=in_address)
            self.mem.handle_remove()
            self.process_close()
            return True
        return False

    def memory_enum_from_to(self, in_from: c_uint64 = 0, in_to: c_uint64 = 0x00007fffffffffff):
        if self.process_open(in_access=win32con.PROCESS_QUERY_INFORMATION):
            self.mem.handle_set(self.handle)
            self.mem.enum_memory_from_to(in_from=in_from, in_to=in_to)
            self.mem.handle_remove()
            self.process_close()
            return True
        return False

    def get_dir(self):
        self.process_open(in_access=win32con.PROCESS_QUERY_INFORMATION, in_inherit=False)
        if self.handle:
            self.file_dir = win32api.GetModuleFileNameW(self.handle)
            self.process_close()
            return True
        else:
            return False

    def process_open(self, in_access: c_int = win32con.PROCESS_QUERY_LIMITED_INFORMATION, in_inherit: c_bool = False) -> bool:
        if not self.pe:
            return False
        try:
            self.handle = OpenProcess(in_access, in_inherit, self.pe.th32ProcessID)
            if not self.handle:
                self.handle = None
                return False
        except Exception as e:
            return False
        return True

    def process_close(self):
        CloseHandle(self.handle)
        self.handle = None

    def process_read(self, in_offset: c_uint64, in_len: c_size_t) -> bool:
        mem_buff    = (c_char * in_len.value)(0)
        bytesReaded = c_uint64(0)
        self.process_open(in_access=win32con.PROCESS_VM_READ)
        if not self.handle:
            return False
        if not GWReadProcessMemory(self.handle, in_offset.value, mem_buff, in_len.value, bytesReaded):
            self.process_close()
            return False
        print(bytesReaded.value)
        if bytesReaded.value > 0:
            self.mem_buff = bytearray(mem_buff)
            return True
        return False


