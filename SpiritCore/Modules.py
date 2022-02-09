from SpiritCore.System import *
from SpiritCore.Payload import *
from SpiritCore.Session import *

def to_unicode(obj):
	return obj
class Modules:
    LoadStatus=False
    Name=""
    Object=None
    SCO=None
    ruler="-"
    Parameate={}
    Payload=None
    UsePayload=False
    PayloadName=""
    configuration=True
    Status=0
    
    def ExploitInit(self):
        SetKey = []
        self.Parameate={}
        for key in sorted(self.Object.Values):
            self.Parameate.update({key:self.Object.Values[key]})
        if self.Object.UsePayload == True:
            for key in sorted(self.Object.PayloadParameate):
                self.Parameate.update({key:self.Object.PayloadParameate[key]})
                self.Object.UsePayloadObject.Parameate.update({key:self.Object.PayloadParameate[key]})
        try:
            if self.Object.UseModulesObject.DEFINE:
                self.condition = self.Object.UseModulesObject.DEFINE.keys()
                for key in self.condition:
                    try:
                        Tiao = self.Object.UseModulesObject.DEFINE[key]
                    except:
                        pass
                    Tiao = self.Object.UseModulesObject.DEFINE[key]
                    TiaoKey = list(Tiao.keys())[0]

                    if self.Object.Values[TiaoKey] == Tiao[TiaoKey]:
                        for key in sorted(self.Object.DEFINE[TiaoKey].Values):
                            #write(key)
                            self.Parameate.update({key: str(self.Object.DEFINE[TiaoKey].Values[key])})
        
        
            
        except Exception as error:
            pass
        try:
            if self.Object.UsePayloadObject.Support==True:
                self.Payload=PayloadData()
                SCO=ShellCode(self.Object,self.Object.UsePayloadObject.Name,self.Parameate)
                self.SCO=SCO
                self.Payload.PayloadData= SCO.raw_shellcode()
                self.Payload.Name =SCO.PayloadName
                self.Payload.Length=len(self.Payload.PayloadData)
        
            else:
                pass
        except:
            pass
        try:
            spacer=""
            if self.configuration:
                write("\n")
                write("Modules ::%s"% self.Name)
                write("="*len("Modules ::%s"% self.Name))
                pattern = '%s%%s  %%s  ' % (spacer)
                key_len = len(max(self.Parameate, key=len))
                if key_len < 4: key_len = 4
                try:
                    val_len = len(max([to_unicode(self.Parameate[x]) for x in self.Parameate], key=len))
                except Exception:
                    val_len = 13
                if val_len < 13: val_len = 13
                write('')
                write(pattern % ('Name'.ljust(key_len), 'Value'.ljust(val_len)))
                write(pattern % (self.ruler * key_len, (self.ruler * 13).ljust(val_len)))
                for key in sorted(self.Parameate):
                    #print_error(str(key))
                    value = self.Parameate[key] if self.Parameate[key] != None else ""
                    try:
                        write(pattern % (
                        key.ljust(key_len), to_unicode(str(value)).ljust(val_len)))
                    except Exception as error:
                        write(error)
                        #self.clear()
                write('')
            else:
                write('\n%sNo options available for this module\n' % (spacer))
        except Exception as error:
            print_error(error.__str__())
        #write(self.Parameate)
        #write(self.Parameate)
    def Init(self,Object):
        self.Object=Object
    def SessionStart(self):
        SessionObj = Session(self.Object)
        SessionObj.TargetOS =self.Object.UsePayloadObject.OS
        SessionObj.PayloadType=self.Object.UsePayloadObject.Types
        SessionObj.SObject=self.Object
        WriteLogs("Call Payload the Handler %s"%self.Object.UsePayloadObject.Name)
        SessionObj.start()
        try:
            SessionObj.Console("")
        except Exception as error:
            write("Error Handler:Exploit:30")
            print_error(error.__str__())
            return
    def GSCOBJECT(self):
        return ShellCode(self.Object,self.Object.UsePayloadObject.Name,self.Parameate)
    