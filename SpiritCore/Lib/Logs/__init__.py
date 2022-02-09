from SpiritCore.Lib.Lib import *




def GetLogsPath():
    if(Win32Platform):
        Path="%s\\Logs"%GetPath()
    else:
        Path="%s/Logs"%GetPath()
    return Path


def MakeLogsPath(FilePath):
    if(Win32Platform):
        Path="%s\\Logs"%GetPath()
        Path+="\\"
        Path+="\\".join(FilePath)
    else:
        Path="%s/Logs"%GetPath()
        Path+="/"
        Path+="/".join(FilePath)
    return Path

def MakePath(FilePath,Paths=""):
    if Paths=="":
        Path=""%GetPath()
    else:
        Path=Paths
    if(Win32Platform):
        Path+="\\"
        Path+="\\".join(FilePath)
    else:
        Path+="/"
        Path+="/".join(FilePath)
    return Path
    