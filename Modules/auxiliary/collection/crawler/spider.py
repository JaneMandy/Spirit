from os import PathLike
from SpiritCore.Modules import *
from SpiritCore.Lib.IPy import IP
import subprocess
from SpiritCore.Lib.Lib import *
from SpiritCore.Lib.Logs import *
import uuid,json
Description="""Network Crawler useing rad
"""
class Module(Modules):
    Info = {
        "Name": "Crawler Scanner ",
        "Author": "ZSD",
        "Description": "Crawler Scanner Support Proxy Scan ",
        "Options": (
            ("URL", "http://14.21.19.49:8081/", True, 'Target URL or Address', None),
            ("HttpProxy", "", True, 'Proxy Options'),
        ),
    }
    def Exploit(self):
        SpiritPath=GetPath()
        BinPath=GetBinPath()
        LogsFile=""
        RadPath=""
        
        if(Win32Platform):
            RadPath = "%s\\rad.exe" %BinPath
            LogsFile="%s\\Logs\\%s"%(SpiritPath,"%s-RAD.json"%uuid.uuid4())
        else:
            RadPath = "%s/rad" %BinPath
            LogsFile="%s/Logs/%s"%(SpiritPath,"%s-RAD.json"%uuid.uuid4())
        print_msg("Rad Path:%s"%RadPath)
        print_msg("Logs File:%s"%LogsFile)
        WriteLogs("Spider Target URL:%s using rad ,RAD Logs%s"%(self.Parameate["URL"],LogsFile))
        RunCommand=[]
        RunCommand.append(RadPath)
        RunCommand.append("-t")
        RunCommand.append(self.Parameate["URL"])
        RunCommand.append("--json-output")
        RunCommand.append(LogsFile)
        if(self.Parameate["HttpProxy"]!=""):
            Proxy=self.Parameate["HttpProxy"]
            print_msg("Enable Proxy HTTP:%s"%Proxy)
            RunCommand.append("--http-proxy")
            RunCommand.append(Proxy)
        print_msg("Command:%s"%" ".join(RunCommand))
        WriteLogs("RAD Run Command:%s"%" ".join(RunCommand))
        CallProcess=subprocess.Popen(" ".join(RunCommand), shell=True,cwd="Logs",stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        CallProcess.wait()
        WriteLogs("-------------------------------------------Spider---------------------------------------------------")
        try:
            JSON=json.loads(open(LogsFile,"r").read())
            for data in JSON:
                write("\n")
                try:
                    print_msg("URL:%s"%data["URL"])
                    write("\tMethod:%s"%data["Method"])
                    write("\tHeader:%s"%data["Header"])
                    try:
                        write("\tCookie:%s"%data["Cookie"])
                    except:
                        pass
                    write("\tUser-Agent:%s"%data["User-Agent"])
                except:
                    pass
        except:
            pass
        write("\n")
        WriteLogs("-----------------------------------------------------------------------------------------------------")