from ctypes import windll, c_void_p, POINTER, c_size_t, Structure, c_uint64, c_uint32, sizeof, c_wchar, c_wchar_p, byref
from ctypes.wintypes import DWORD
from pprint import pprint

from inc.errors import GWErrors
from inc.system_info import GWSystemInfo



class MEMORY_BASIC_INFORMATION(Structure):
    """https://msdn.microsoft.com/en-us/library/aa366775"""
    _fields_ = (('BaseAddress',         c_uint64),
                ('AllocationBase',      c_uint64),
                ('AllocationProtect',   DWORD),
                ('RegionSize',          c_size_t),
                ('State',               DWORD),
                ('Protect',             DWORD),
                ('Type',                DWORD))


MEM_COMMIT              =   0x1000
MEM_FREE                =   0x10000
MEM_RESERVE             =   0x2000


MEM_IMAGE               =   0x1000000
MEM_MAPPED              =   0x40000
MEM_PRIVATE             =   0x20000


PAGE_EXECUTE            =   0x10
PAGE_EXECUTE_READ       =   0x20
PAGE_EXECUTE_READWRITE  =   0x40
PAGE_EXECUTE_WRITECOPY  =   0x80
PAGE_NOACCESS           =   0x01
PAGE_READONLY           =   0x02
PAGE_READWRITE          =   0x04
PAGE_WRITECOPY          =   0x08
PAGE_TARGETS_INVALID    =   0x40000000
PAGE_TARGETS_NO_UPDATE  =   0x40000000
PAGE_GUARD              =   0x100
PAGE_NOCACHE            =   0x200
PAGE_WRITECOMBINE       =   0x400


VirtualQueryEx                 = windll.kernel32.VirtualQueryEx
VirtualQueryEx.argtypes        = [ c_void_p, c_void_p, POINTER(MEMORY_BASIC_INFORMATION), c_size_t ]
VirtualQueryEx.rettype         = c_size_t

# StrFormatByteSizeW
StrFormatByteSize                 = windll.shlwapi.StrFormatByteSizeW
StrFormatByteSize.argtypes        = [ c_uint64, POINTER(c_wchar), c_uint32 ]
StrFormatByteSize.rettype         = c_wchar_p


class GWVirtualMemory:

    si:     GWSystemInfo    =   None
    memory: dict            =   dict()
    err:    GWErrors        =   GWErrors()
    handle                  =   None
    count:  int             =   0
    size:   c_uint64        =   0

    # ##########################################################################
    #   Constructor
    # ##########################################################################
    def __init__(self, handle: c_void_p = None, si: GWSystemInfo = None):
        self.clear_memory_list()
        if handle:
            self.handle = handle
        if si is not None:
            self.si = si
        else:
            self.si = GWSystemInfo()

    # ##########################################################################
    #   Clear list
    # ##########################################################################
    def clear_memory_list(self):
        self.memory = dict()

    # ##########################################################################
    #   Set handle
    # ##########################################################################
    def handle_set(self, in_handle):
        self.handle = in_handle

    # ##########################################################################
    #   Removes handle
    # ##########################################################################
    def handle_remove(self):
        self.handle = None

    # ##########################################################################
    #   Get's MEMORY_BASIC_INFORMATION by Address
    # ##########################################################################
    def get_memory_information_by_address(self, in_address: c_uint64 = 0):
        if not self.handle:
            return False
        mbi: MEMORY_BASIC_INFORMATION = MEMORY_BASIC_INFORMATION()
        size = sizeof(mbi)
        ret = VirtualQueryEx(self.handle, in_address, mbi, size)
        if not ret:
            return False
        return mbi

    # ##########################################################################
    #   Get's list of MEMORY_BASIC_INFORMATION
    # ##########################################################################
    def enum_memory_from_to(self, in_from: c_uint64 = 0, in_to: c_uint64 = 0):
        self.clear_memory_list()
        if not self.handle:
            return False
        # print(self.si)
        addr_max: c_uint64 = in_to
        addr_min: c_uint64 = in_from
        if addr_max  < self.si.lpMaximumApplicationAddress:
            addr_max = self.si.lpMaximumApplicationAddress - 1
        if addr_min  < self.si.lpMinimumApplicationAddress:
            addr_min = self.si.lpMinimumApplicationAddress + 1

        address = addr_min
        pid = windll.kernel32.GetProcessId(self.handle)
        while address < addr_max:
            mbi = self.get_memory_information_by_address(address)
            if mbi is not False:
                addr_base: c_uint64 = c_uint64(mbi.BaseAddress)
                addr_len:  c_uint64 = c_uint64(mbi.RegionSize)
                if ( mbi.State and MEM_COMMIT ) and (mbi.Protect and PAGE_READWRITE ):
                    self.memory[mbi.BaseAddress] = mbi
                address = addr_base.value + addr_len.value + 1
            else:
                print("Error: {} Base: 0x{:016X}".format(
                    self.err.get_error_string(),
                    address
                ))
                return False
        self.count = len(self.memory)
        self.size  = 0
        for m in self.memory.keys():
            m: dict = m
            self.size += self.memory[m].RegionSize

    # ##########################################################################
    # Get count in list
    # ##########################################################################
    def get_count(self):
        return self.count

    # ##########################################################################
    # Get Size in Bytes
    # ##########################################################################
    def get_size_in_byte(self):
        # s = (c_wchar * 8192)(0)
        # StrFormatByteSize(self.size, byref(c_wchar), 8192)
        # print(c_wchar)
        return self.get_sizeof_fmt(self.size)

    # ##########################################################################
    #
    # ##########################################################################
    def get_sizeof_fmt(self, num, suffix='B'):
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f %s%s" % (num, 'Yi', suffix)

    # ##########################################################################
    #
    # ##########################################################################
    # ##########################################################################
    #
    # ##########################################################################
