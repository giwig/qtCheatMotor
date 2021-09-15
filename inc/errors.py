from ctypes import WinDLL, windll, c_void_p, c_uint64, c_uint32, c_wchar_p, c_wchar, create_string_buffer, POINTER, byref

from ctypes.wintypes import LPWSTR

# GetLastError
GetLastError                 = windll.kernel32.GetLastError
GetLastError.argtypes        = [  ]
GetLastError.rettype         = c_uint64


FORMAT_MESSAGE_ALLOCATE_BUFFER  =   0x00000100
FORMAT_MESSAGE_ARGUMENT_ARRAY   =   0x00002000
FORMAT_MESSAGE_FROM_HMODULE     =   0x00000800
FORMAT_MESSAGE_FROM_STRING      =   0x00000400
FORMAT_MESSAGE_FROM_SYSTEM      =   0x00001000
FORMAT_MESSAGE_IGNORE_INSERTS   =   0x00000200

# FormatMessage
FormatMessage                 = windll.kernel32.FormatMessageW
FormatMessage.argtypes        = [ c_uint64, c_void_p, c_uint64, c_uint64, POINTER(c_wchar_p), c_uint64, c_void_p ]
FormatMessage.rettype         = c_uint64


LANG_NEUTRAL = 0x00
SUBLANG_NEUTRAL = 0x00
SUBLANG_DEFAULT = 0x01

LANG_ENGLISH = 0x09
SUBLANG_ENGLISH_US = 0x01
def MAKELANGID(primary, sublang):
    return (primary & 0xFF) | (sublang & 0xFF) << 16

LCID_ENGLISH = MAKELANGID(LANG_ENGLISH, SUBLANG_ENGLISH_US)
LCID_DEFAULT = MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT)
LCID_NEUTRAL = MAKELANGID(LANG_NEUTRAL, SUBLANG_NEUTRAL)
assert LCID_NEUTRAL == 0


class GWErrors:

    msg:    str         =   None
    msgID:  int         =   0

    def __init__(self):
        pass

    def get_last_error(self):
        self.msgID = GetLastError()
        return self.msgID

    def get_error_string(self):
        self.clear()
        buf: LPWSTR = LPWSTR()
        chars = FormatMessage(
            FORMAT_MESSAGE_ALLOCATE_BUFFER |
            FORMAT_MESSAGE_FROM_SYSTEM |
            FORMAT_MESSAGE_IGNORE_INSERTS,
            0,
            self.get_last_error(),
            LCID_DEFAULT,
            byref(buf),
            0,
            0
        )
        self.msg = str(buf.value)
        return self.msg

    def clear(self):
        self.msgID  = -1
        self.msg    = ""

