#!/bin/python

from ctypes import Structure, byref, windll, POINTER, c_uint64, c_uint32, sizeof
from ctypes.wintypes import WORD, DWORD, LPVOID, HANDLE, PBOOL, BOOL, USHORT
from inc.errors import GWErrors


class SYSTEM_INFO(Structure):
    _fields_ = [
        ("wProcessorArchitecture",      WORD),
        ("wReserved",                   WORD),
        ("dwPageSize",                  DWORD),
        ("lpMinimumApplicationAddress", LPVOID),
        ("lpMaximumApplicationAddress", LPVOID),
        ("dwActiveProcessorMask",       DWORD),
        ("dwNumberOfProcessors",        DWORD),
        ("dwProcessorType",             DWORD),
        ("dwAllocationGranularity",     DWORD),
        ("wProcessorLevel",             WORD),
        ("wProcessorRevision",          WORD),
    ]


# GetSystemInfo
GetSystemInfo                   = windll.kernel32.GetSystemInfo
GetSystemInfo.argtypes          = [ POINTER(SYSTEM_INFO) ]
GetSystemInfo.reltype           = None

# GetNativeSystemInfo
GetNativeSystemInfo             = windll.kernel32.GetNativeSystemInfo
GetNativeSystemInfo.argtypes    = [ POINTER(SYSTEM_INFO) ]
GetNativeSystemInfo.reltype     = None

# IsWow64Process
IsWow64Process                  = windll.kernel32.IsWow64Process
IsWow64Process.argtypes         = [ HANDLE, PBOOL ]
IsWow64Process.reltype          = BOOL

# BOOL IsWow64Process2(
#   HANDLE hProcess,
#   USHORT *pProcessMachine,
#   USHORT *pNativeMachine
# );
IsWow64Process2                  = windll.kernel32.IsWow64Process2
IsWow64Process2.argtypes         = [ HANDLE, USHORT, USHORT ]
IsWow64Process2.reltype          = BOOL

class GWSystemInfo:

    err:            GWErrors    = GWErrors()
    system_info:    SYSTEM_INFO = SYSTEM_INFO()

    wProcessorArchitecture:         DWORD       =   0
    dwPageSize:                     DWORD       =   0
    lpMinimumApplicationAddress:    c_uint64    =   0
    lpMaximumApplicationAddress:    c_uint64    =   0
    dwActiveProcessorMask:          c_uint64    =   0
    dwNumberOfProcessors:           DWORD       =   0
    dwProcessorType:                DWORD       =   0
    dwAllocationGranularity:        DWORD       =   0
    wProcessorLevel:                WORD        =   0
    wProcessorRevision:             WORD        =   0

    def __init__(self):
        self.get_system_info()
        # print(self.system_info)

    def get_system_info(self):
        si = SYSTEM_INFO(0)
        # print("SYSTEM_INFO Size: {}".format(sizeof(SYSTEM_INFO)))

        GetNativeSystemInfo(byref(si))

        self.system_info = si

        self.wProcessorArchitecture         =   si.wProcessorArchitecture
        self.dwPageSize                     =   si.dwPageSize
        self.lpMinimumApplicationAddress    =   si.lpMinimumApplicationAddress
        self.lpMaximumApplicationAddress    =   si.lpMaximumApplicationAddress
        self.dwActiveProcessorMask          =   si.dwActiveProcessorMask
        self.dwNumberOfProcessors           =   si.dwNumberOfProcessors
        self.dwProcessorType                =   si.dwProcessorType
        self.dwAllocationGranularity        =   si.dwAllocationGranularity
        self.wProcessorLevel                =   si.wProcessorLevel
        self.wProcessorRevision             =   si.wProcessorRevision

    def print_system_info(self):
        print("{}".format(self.wProcessorArchitecture))


