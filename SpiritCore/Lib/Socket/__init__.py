from SpiritCore.System import *
from socket import *
import sys,re,os
class Socket(socket):
    Ip={}
    Port=0
    Bind=True
    def __init__(self,Ip,Port,Bind=True):
        socket.__init__(self)
        self.settimeout(0.5)
        self.Bind=Bind
        self.Ip=Ip
        self.Port=Port
    def Connect(self):
        if self.Bind==True:

            self.connect((self.Ip,self.Port))

        elif self.Bind==False:
            pass
    def Send(self,Data):
        try:
            if sys.version_info.major == 3:
                self.send(Data.encode('gbk'))
                #print(Data)
            elif sys.version_info.major == 2:
                self.Send(Data)
        except Exception as error:
            print(error)
    def Recv(self,Size):
        if sys.version_info.major == 3:
            return str(self.recv(Size),encoding="gbk")
                # print(Data)
        elif sys.version_info.major == 2:
            return  self.recv(Size)
