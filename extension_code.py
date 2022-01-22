import types as _types
import ctypes as _ctypes
from ctypes import wintypes as _wtypes
_mtypes = _types.ModuleType('_mtypes')

_ole32 = _ctypes.WinDLL('ole32')
_shell32 = _ctypes.WinDLL('shell32')
_user32 = _ctypes.WinDLL('user32')

try:
    from win32com.shell import shell as _shell
except ImportError:
    _shell = None

try:
    from win32com.shell import shellcon
except ImportError:
    shellcon = _types.ModuleType('shellcon')
    shellcon.SHGFI_LARGEICON         = 0x00000
    shellcon.SHGFI_SMALLICON         = 0x00001
    shellcon.SHGFI_OPENICON          = 0x00002
    shellcon.SHGFI_SHELLICONSIZE     = 0x00004
    shellcon.SHGFI_PIDL              = 0x00008
    shellcon.SHGFI_USEFILEATTRIBUTES = 0x00010
    shellcon.SHGFI_ICON              = 0x00100
    shellcon.SHGFI_DISPLAYNAME       = 0x00200
    shellcon.SHGFI_TYPENAME          = 0x00400
    shellcon.SHGFI_ATTRIBUTES        = 0x00800
    shellcon.SHGFI_ICONLOCATION      = 0x01000
    shellcon.SHGFI_EXETYPE           = 0x02000
    shellcon.SHGFI_SYSICONINDEX      = 0x04000
    shellcon.SHGFI_LINKOVERLAY       = 0x08000
    shellcon.SHGFI_SELECTED          = 0x10000
    shellcon.SHGFI_ATTR_SPECIFIED    = 0x20000

try:
    import win32con
except ImportError:
    win32con = _types.ModuleType('win32con')
    win32con.MAX_PATH = 260
    win32con.FILE_ATTRIBUTE_READONLY            = 0x00001
    win32con.FILE_ATTRIBUTE_HIDDEN              = 0x00002
    win32con.FILE_ATTRIBUTE_SYSTEM              = 0x00004
    win32con.FILE_ATTRIBUTE_DIRECTORY           = 0x00010
    win32con.FILE_ATTRIBUTE_ARCHIVE             = 0x00020
    win32con.FILE_ATTRIBUTE_DEVICE              = 0x00040
    win32con.FILE_ATTRIBUTE_NORMAL              = 0x00080
    win32con.FILE_ATTRIBUTE_TEMPORARY           = 0x00100
    win32con.FILE_ATTRIBUTE_ATOMIC_WRITE        = 0x00200
    win32con.FILE_ATTRIBUTE_SPARSE_FILE         = 0x00200
    win32con.FILE_ATTRIBUTE_REPARSE_POINT       = 0x00400
    win32con.FILE_ATTRIBUTE_XACTION_WRITE       = 0x00400
    win32con.FILE_ATTRIBUTE_COMPRESSED          = 0x00800
    win32con.FILE_ATTRIBUTE_OFFLINE             = 0x01000
    win32con.FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 0x02000
    win32con.FILE_ATTRIBUTE_ENCRYPTED           = 0x04000
    win32con.FILE_ATTRIBUTE_VIRTUAL             = 0x10000

_mtypes.CData = _ctypes.Array.__bases__[0]
_mtypes.PPIDLIST_ABSOLUTE = _ctypes.POINTER(_ctypes.c_void_p)
_mtypes.SFGAOF = _wtypes.ULONG
_mtypes.PSFGAOF = _ctypes.POINTER(_mtypes.SFGAOF)

_ole32.CoInitialize.restype = _ctypes.HRESULT # checked
_ole32.CoInitialize.argtypes = (_ctypes.c_void_p,)
_ole32.CoUninitialize.restype = None
_ole32.CoUninitialize.argtypes = ()
_ole32.CoTaskMemFree.restype = None
_ole32.CoTaskMemFree.argtypes = (_ctypes.c_void_p,)
_user32.DestroyIcon.argtypes = (_wtypes.HICON,)

_shell32.SHParseDisplayName.restype = _ctypes.HRESULT # checked
_shell32.SHParseDisplayName.argtypes = (
    _wtypes.LPCWSTR,           # pszName,   _In_
    _ctypes.c_void_p,          # pbc,       _In_opt_
    _mtypes.PPIDLIST_ABSOLUTE, # ppidl,     _Out_
    _mtypes.SFGAOF,            # sfgaoIn,   _In_
    _mtypes.PSFGAOF)           # psfgaoOut, _Out_opt_

class SHFILEINFO(_ctypes.Structure):
   _fields_ = (('hIcon', _wtypes.HICON),
               ('iIcon', _ctypes.c_int),
               ('dwAttributes', _wtypes.DWORD),
               ('szDisplayName', _wtypes.WCHAR * win32con.MAX_PATH),
               ('szTypeName', _wtypes.WCHAR * 80))

_mtypes.SHFILEINFO = SHFILEINFO
_mtypes.PSHFILEINFO = _ctypes.POINTER(SHFILEINFO)

_shell32.SHGetFileInfoW.restype = _ctypes.c_void_p
_shell32.SHGetFileInfoW.argtypes = (
    _wtypes.LPVOID,      # pszPath,          _In_
    _wtypes.DWORD,       # dwFileAttributes,
    _mtypes.PSHFILEINFO, # psfi,             _Inout_
    _wtypes.UINT,        # cbFileInfo,
    _wtypes.UINT)        # uFlags

def SHGetFileInfo(pidl, attributes=0, flags=0):
    if _shell is not None:
        if not isinstance(pidl, (str, bytes, _mtypes.CData)):
            pidl = _shell.PIDLAsString(pidl)
    finfo = SHFILEINFO()
    _ole32.CoInitialize(None)    
    try:
        retval = _shell32.SHGetFileInfoW(pidl,
                                         attributes,
                                         _ctypes.byref(finfo),
                                         _ctypes.sizeof(finfo),
                                         flags)
    finally:
        _ole32.CoUninitialize()
    if not retval:            
        if flags != shellcon.SHGFI_EXETYPE:
            raise _ctypes.WinError()
    return retval, finfo


if __name__ == '__main__':
    import os    
    path = os.path.expanduser(r'~\Desktop\desktop.ini')
    pidl = _shell.SHParseDisplayName(path, 0)[0]
    assert isinstance(pidl, list)

    flags = (shellcon.SHGFI_PIDL |
             shellcon.SHGFI_ICON |
             shellcon.SHGFI_DISPLAYNAME |
             shellcon.SHGFI_TYPENAME |
             shellcon.SHGFI_ATTRIBUTES |
             shellcon.SHGFI_SYSICONINDEX)

    hImageList, finfo = SHGetFileInfo(pidl, 0, flags)

    print('hImageList:', hImageList)
    for name, typ in finfo._fields_:
        print(name, ': ', getattr(finfo, name))

    if finfo.hIcon:
        _user32.DestroyIcon(finfo.hIcon)
