from ctypes import windll, c_void_p, POINTER, c_size_t, Structure, c_uint64, c_uint32, sizeof
from ctypes.wintypes import DWORD
from pprint import pprint

from inc.errors import GWErrors


class MEMORY_BASIC_INFORMATION(Structure):
    """https://msdn.microsoft.com/en-us/library/aa366775"""
    _fields_ = (('BaseAddress', c_void_p),
                ('AllocationBase',    c_void_p),
                ('AllocationProtect', DWORD),
                ('RegionSize', c_size_t),
                ('State',   DWORD),
                ('Protect', DWORD),
                ('Type',    DWORD))


VirtualQueryEx                 = windll.kernel32.VirtualQueryEx
VirtualQueryEx.argtypes        = [ c_void_p, c_void_p, POINTER(MEMORY_BASIC_INFORMATION), c_size_t ]
VirtualQueryEx.rettype         = c_size_t


class GWVirtualMemory:

    memory: list[MEMORY_BASIC_INFORMATION]  = None
    err:    GWErrors                        = GWErrors()

    def __init__(self, handle: c_void_p = None):
        if handle:
            self.handle = handle

    def handle_set(self, in_handle):
        self.handle = in_handle

    def handle_remove(self):
        self.handle = None

    def get_memory_information_by_address(self, in_address: c_uint64 = 0):
        if not self.handle:
            return False
        mbi: MEMORY_BASIC_INFORMATION = MEMORY_BASIC_INFORMATION()
        size = sizeof(mbi)
        ret = VirtualQueryEx(self.handle, in_address, mbi, size)
        # print("Base == 0x{:X}".format(
        #     mbi.BaseAddress,
        # ))
        if not ret:
            return False
        return mbi

    def enum_memory_from_to(self, in_from: c_uint64 = 0, in_to: c_uint64 = 0x7fffffffffffffff):
        if not self.handle:
            return False
        address = in_from
        while address < in_to:
            mbi = self.get_memory_information_by_address(address)
            if mbi:
                self.err.get_error_string()
                print("Error == {}".format(self.err.msg))

                print(type(mbi))
                print("{:X} {:X} current == {:X}".format(in_from, in_to, address))
                pprint(mbi)
                addr_base: c_uint64   =   c_uint64(mbi.BaseAddress)
                addr_len:  c_uint64   =   c_uint64(mbi.RegionSize)
                address     =   addr_base + addr_len + 1
                self.memory.append(mbi)
            else:
                address += 0x1000

