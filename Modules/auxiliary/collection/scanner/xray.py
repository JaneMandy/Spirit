from os import PathLike
from SpiritCore.Modules import *
from SpiritCore.Lib.IPy import IP
import subprocess
from SpiritCore.Lib.Lib import *
from SpiritCore.Lib.Logs import *
import uuid,json,time
Description="""WebScan useing xrat
"""
class Module(Modules):
    Info = {
        "Name": "WebScan Scanner ",
        "Author": "ZSD",
        "Description": "WebScan Scanner Support Proxy Scan ",
        "Options": (
            ("URL", "http://14.21.19.49:8081/", True, 'Target URL or Address', None),
        ),
    }
    def Exploit(self):
        SpiritPath=GetPath()
        BinPath=GetBinPath()
        LogsFile=""
        RadPath=""
        XaryPath=""
        if(Win32Platform):
            XaryPath = "%s\\xray.exe" %BinPath
            RadPath = "%s\\rad.exe" %BinPath
            LogsFile="%s\\Logs\\%s"%(SpiritPath,"%s-XRAY.json"%uuid.uuid4())
        else:
            XaryPath = "%s/xray" %BinPath
            RadPath = "%s/rad" %BinPath
            LogsFile="%s/Logs/%s"%(SpiritPath,"%s-XRAY.json"%uuid.uuid4())
        print_msg("Rad Path:%s"%RadPath)
        print_msg("Logs File:%s"%LogsFile)
        XrayRunComand=[]
        XrayRunComand.append(XaryPath)
        XrayRunComand.append("webscan")
        XrayRunComand.append("--listen")
        XrayRunComand.append("127.0.0.1:8888")
        XrayRunComand.append("--json-output")
        XrayRunComand.append(LogsFile)
        WriteLogs("Xray Run Command:%s"%" ".join(XrayRunComand))
        XrayObj=subprocess.Popen(XrayRunComand,cwd="Logs")
        time.sleep(5)
        RunCommand=[]
        RunCommand.append(RadPath)
        RunCommand.append("-t")
        RunCommand.append(self.Parameate["URL"])
        RunCommand.append("--http-proxy")
        RunCommand.append("127.0.0.1:8888")
        print_msg("Command:%s"%" ".join(RunCommand))
        WriteLogs("Rad Run Command:%s"%" ".join(RunCommand))
        CallProcess=subprocess.Popen(RunCommand,cwd="Logs")
        try:
            CallProcess.wait()
            XrayObj.wait()
        except:
            pass
        time.sleep(3)
        print_success("Scan Log")
        WriteLogs("-----------------------------------------XRAY SCAN--------------------------------------------------")
        try:
            JSON=json.loads(open(LogsFile,"r").read())
            for Dic in JSON:
                write("\n")
                for x in Dic:
                    write("%s:%s"%(x,Dic[x]))
                        
        except Exception as error:
            pass#write(error)
            
        write("\n")
        WriteLogs("-----------------------------------------------------------------------------------------------------")