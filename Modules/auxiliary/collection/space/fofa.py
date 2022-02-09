
from SpiritCore.System import *
from SpiritCore.Modules import *
from SpiritCore.Config import *
from SpiritCore.Lib.Fofa import *


class Module(Modules):
    Info = {
        "Name": "Fofa Network Space Search",
        "Author": "ZSD",
        "Description": "Fofa Network Space Search",
        "Options": (
            ("SearchText", "app=\"Thinkphp\"", True, 'searchText', None),
            ("PAGE", "1", True, 'SEARCH PAGE', None),
            ("Fields","host,ip,port",True,"Search fields",None)
        ),
    }
    def Exploit(self):
        WriteLogs("Fofa Search Text:%s"%self.Parameate["SearchText"])
        OutputText=""
        Object= FofaAPI(Fofa_Mail,Fofa_Keys)
        results= (Object.get_data(self.Parameate["SearchText"],int(self.Parameate["PAGE"]),fields=self.Parameate["Fields"]))
        try:
            if Object.UserInfo["error"]==True:
                print_error("Error:%s"%Object.UserInfo["errmsg"])
                WriteLogs("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Error!!!!!!!!!!!!!!!!!!!!!!!")
                WriteLogs("!!!!Error:%s"%Object.UserInfo["errmsg"])
                return
        except:
            pass
        print_msg("Search Text:%s"%results["query"])  #results
        print_success("results Count:%d"%len(results["results"]))
        WriteLogs("results Count:%d"%len(results["results"]))
        write("\n")
        write(self.Parameate["Fields"].replace(",","\t"))
        WriteLogs("----------------------------------------Fofa Search Results------------------------------------------")
        for rel in results["results"]:
            OutputText=""
            if type([])==type(rel):
                for text in rel:
                    OutputText+="%s\t"%(text)
                write(OutputText)
            else:
                write(rel)
        WriteLogs("-----------------------------------------------------------------------------------------------------")
        
            
        