from SpiritCore.System import *



class Modules:
    LoadStatus=False
    Name=""
    Object=None
    Parameate={}
    PayloadBuffer=None
    UsePayload=False
    PayloadName=""
    Status=0
    def ExploitInit(self):
        SetKey = []
        self.Parameate={}
        for key in sorted(self.Object.Values):
            self.Parameate.update({key:self.Object.Values[key]})
        if self.Object.UsePayload == True:
            for key in sorted(self.Object.PayloadParameate):
                self.Parameate.update({key:self.Object.PayloadParameate[key]})
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

                    if self.Object.Values[TiaoKey] != Tiao[TiaoKey]:
                        for key in sorted(self.Object.DEFINE[TiaoKey].Values):
                            #print(key)
                            self.Parameate.update({key: str(self.Object.DEFINE[TiaoKey].Values[key])})
        except Exception as error:
            pass
        #print(self.Parameate)
        #print(self.Parameate)
    def Init(self,Object):
        self.Object=Object
    def Payload(self):
        pass
    