ProxyType  = ["NO","HTTP","HTTPS","SOCK5","SOCK4","SpiritProxy"]

import sys,os

Win32Platform = (sys.platform == "win32")

def GetPath():
    return sys.path[0]


def GetBinPath():
    if(Win32Platform):
        Path="%s\\SpiritCore\\Lib\\Bin\\Windows"%GetPath()
    else:
        Path="%s/SpiritCore/Lib/Bin/Linux"%GetPath()
    return Path


<<<<<<< HEAD










=======
>>>>>>> 9dbce14cb0e4785b049f67e3bb46f02c4c305560
