#!/usr/bin/env python3
# coding=utf-8



from SpiritCore.Spirit import *
from SpiritCore.Lib.Logs import *
from SpiritCore.Lib.gol import *

import  uuid 

LogsFilePath=""


golinit()
if __name__=="__main__":
    
    LogsFilePath=MakeLogsPath(["Spirit-Console-%s.log"%(uuid.uuid4())])
    set_value('LogsFilePath',LogsFilePath)
    WriteLogs("Start Run Framework")
    Obj=Framework()
    WriteLogs("Framework Load Success")
    Obj.Init()



















