#!/bin/python

from ctypes import c_uint64, windll, c_uint32, c_void_p, c_char, Structure, c_long, c_ulong, POINTER, sizeof, c_size_t, \
    c_wchar, c_int, c_bool, WinDLL
from ctypes.wintypes import *

import win32api
import win32con
from hexdump import hexdump


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


## Process32FirstW
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


_exdll = windll.kernel32

def _psapifunc(fname):
    global _exdll
    try: return getattr(_exdll, fname)
    except:
        try:
            return getattr('K32' + _exdll, fname)
        except:
            if 'psapi' in _exdll._name: raise
            _exdll = WinDLL('psapi.dll')
            return _psapifunc(fname)


# GetModuleFileNameExA = _psapifunc('GetModuleFileNameExA')
GetModuleFileNameExW = _psapifunc('GetModuleFileNameExW')

GetModuleFileNameExW.restype         = GetModuleFileNameExW.restype = c_uint64
GetModuleFileNameExW.argtypes        = [ c_void_p, c_void_p, POINTER(c_wchar), c_uint32]
GetModuleFileNameExW.rettype         = c_uint32


class GWProcess:

    pe:         PROCESSENTRY32W     = None
    exe_name:   str                 = None
    handle:     c_void_p            = None
    mem_buff                        = None
    file_dir:   str                 = None

    def __init__(self, pe: PROCESSENTRY32W = None):
        if pe:
            self.pe = pe
            self.get_dir()

    def set_pe(self, pe: PROCESSENTRY32W = -1):
        self.pe = pe

    def get_pe(self) -> PROCESSENTRY32W:
        return self.pe

    def get_pid(self) -> int:
        return self.pe.th32ProcessID

    def get_memdump(self, in_off = 0) -> str:
        return hexdump(self.mem_buff, off=in_off)

    def get_dir(self):
        # if self.process_open(in_access=c_int( PROCESS_QUERY_INFORMATION and PROCESS_VM_READ )):
        #     mem = (c_wchar * MAX_PATH)(0)
        handle = win32api.OpenProcess(win32con.PROCESS_VM_READ, False, self.pe.th32ProcessID)
        self.file_dir = win32api.GetModuleFileNameW(handle)

        # if GetModuleFileNameExW(self.handle, 0, mem, MAX_PATH):
        #     self.file_dir = str(mem.value)
        # else:
        #     print("No dir")
        # self.process_close()

    def process_open(self, in_access: c_int = PROCESS_ALL_ACCESS, in_inherit: bool = False) -> bool:
        if not self.pe:
            return False
        # self.handle = OpenProcess(in_access, in_inherit, self.pe.th32ProcessID)
        if not self.handle:
            return False
        return True

    def process_close(self):
        CloseHandle(self.handle)

    def process_read(self, in_offset: c_uint64, in_len: c_size_t) -> bool:
        mem_buff    = (c_char * in_len.value)(0)
        bytesReaded = c_uint64(0)
        if GWReadProcessMemory(self.handle, in_offset.value, mem_buff, in_len.value, bytesReaded):
            print(bytesReaded)
            if bytesReaded.value >= c_uint64(0).value:
                self.mem_buff = bytearray(mem_buff)
                return True
        return False


