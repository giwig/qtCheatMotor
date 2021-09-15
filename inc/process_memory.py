from ctypes import windll, c_void_p, POINTER, c_size_t, Structure, c_uint64, c_uint32, sizeof
from ctypes.wintypes import DWORD
from pprint import pprint

from inc.errors import GWErrors


class MEMORY_BASIC_INFORMATION(Structure):
    """https://msdn.microsoft.com/en-us/library/aa366775"""
    _fields_ = (('BaseAddress',         c_uint64),
                ('AllocationBase',      c_uint64),
                ('AllocationProtect',   DWORD),
                ('RegionSize',          c_size_t),
                ('State',               DWORD),
                ('Protect',             DWORD),
                ('Type',                DWORD))


MEM_COMMIT      =   0x1000
MEM_FREE        =   0x10000
MEM_RESERVE     =   0x2000


MEM_IMAGE       =   0x1000000
MEM_MAPPED      =   0x40000
MEM_PRIVATE     =   0x20000


VirtualQueryEx                 = windll.kernel32.VirtualQueryEx
VirtualQueryEx.argtypes        = [ c_void_p, c_void_p, POINTER(MEMORY_BASIC_INFORMATION), c_size_t ]
VirtualQueryEx.rettype         = c_size_t


class GWVirtualMemory:

    memory: list[MEMORY_BASIC_INFORMATION]  =   list()
    err:    GWErrors                        =   GWErrors()
    handle: c_void_p                        =   None

    # ##########################################################################
    #   Constructor
    # ##########################################################################
    def __init__(self, handle: c_void_p = None):
        self.clear_memory_list()
        if handle:
            self.handle = handle

    # ##########################################################################
    #   Clear list
    # ##########################################################################
    def clear_memory_list(self):
        self.memory.clear()

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
    def enum_memory_from_to(self, in_from: c_uint64 = 0, in_to: c_uint64 = 0x00007fffffffffff):
        self.clear_memory_list()
        if not self.handle:
            return False
        address = in_from
        while address < in_to:
            mbi = self.get_memory_information_by_address(address)
            if mbi:
                addr_base: c_uint64 = c_uint64(mbi.BaseAddress)
                addr_len: c_uint64 = c_uint64(mbi.RegionSize)
                if int(mbi.State) is not MEM_FREE: #and mbi.Type is MEM_PRIVATE:
                    self.memory.append(mbi)
                    # print("Address: {:X} Status: {:X}".format(address, mbi.State))
                address                 =   addr_base.value + addr_len.value + 1
            else:
                address += 0x1000
    # ##########################################################################
    #
    # ##########################################################################

