from SpiritCore.Modules import *
from SpiritCore.Lib.IPy import IP
import socket,threading,socks
from SpiritCore.Lib.Lib import *
Description="""Service Scanner
Target Example:
    127.0.0.1
    127.0.0.0/24
Proxy 
    
"""
class Module(Modules):
    Info = {
        "Name": "Port Scanner ",
        "Author": "ZSD",
        "Description": "Port Scanner Support Proxy Scan ",
        "Options": (
            ("Target", "192.168.0.0/24", True, 'Target IP Address', None),
            ("Proxy", "NO", True, 'Proxy Options',ProxyType),
            ("Port", "80,443", True, 'Scan Port ', None),
        ),
        "Proxy":(
            ("ProxyAddress","127.0.0.1",True,"Proxy Server Address"),
            ("ProxyPort"        ,"8080"     ,True,"Proxy Server Port"),
            ("Username","",True,"Proxy Anth Username"),
            ("Password","",True,"Proxy Anth Password"),
        ),
    }
    def Exploit(self):
        print_success("Success")